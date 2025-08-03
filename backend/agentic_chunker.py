import uuid
import os
import time
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
load_dotenv()

class AgenticChunker:
    def __init__(self, gemini_api_key=None):
        self.chunks = {}
        self.id_truncate_limit = 5
        self.generate_new_metadata_ind = True
        self.print_logging = True
        self.api_call_count = 0  # Initialize API call counter
        self.api_limit = 14  # API call limit
        self.pause_duration = 60  # Pause duration in seconds

        if gemini_api_key is None:
            gemini_api_key = os.getenv("GOOGLE_API_KEY")
        if gemini_api_key is None:
            raise ValueError("API key is not provided and not found in environment variables")

        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def _check_api_limit(self):
        if self.api_call_count >= self.api_limit:
            print(f"API call limit reached ({self.api_call_count}). Pausing for {self.pause_duration} seconds...")
            time.sleep(self.pause_duration)
            self.api_call_count = 0  # Reset counter after pause

    def _make_api_call(self, prompt):
        self._check_api_limit()  # Check if we need to pause before making the call
        print(f"Making API call #{self.api_call_count + 1} with prompt: {prompt[:50]}...")
        response = self.model.generate_content(prompt)
        self.api_call_count += 1  # Increment the counter after the call
        print(f"API call #{self.api_call_count} completed.")
        return response.text

    def add_propositions(self, propositions):
        for proposition in propositions:
            self.add_proposition(proposition)

    def add_proposition(self, proposition):
        if self.print_logging:
            print(f"\nAdding: '{proposition}'")

        if len(self.chunks) == 0:
            if self.print_logging:
                print("No chunks, creating a new one")
            self._create_new_chunk(proposition)
            return

        chunk_id = self._find_relevant_chunk(proposition)

        if chunk_id:
            if self.print_logging:
                print(f"Chunk Found ({self.chunks[chunk_id]['chunk_id']}), adding to: {self.chunks[chunk_id]['title']}")
            self.add_proposition_to_chunk(chunk_id, proposition)
        else:
            if self.print_logging:
                print("No chunks found")
            self._create_new_chunk(proposition)

    def add_proposition_to_chunk(self, chunk_id, proposition):
        self.chunks[chunk_id]['propositions'].append(proposition)
        if self.generate_new_metadata_ind:
            self.chunks[chunk_id]['summary'] = self._update_chunk_summary(self.chunks[chunk_id])
            self.chunks[chunk_id]['title'] = self._update_chunk_title(self.chunks[chunk_id])

    def _update_chunk_summary(self, chunk):
        prompt = f"""
        You are the steward of a group of chunks which represent groups of sentences that talk about a similar topic.
        A new proposition was just added to one of your chunks, you should generate a very brief 1-sentence summary which will inform viewers what a chunk group is about.
        A good summary will say what the chunk is about, and give any clarifying instructions on what to add to the chunk.
        Your summaries should anticipate generalization. If you get a proposition about apples, generalize it to food.
        Or month, generalize it to "date and times".

        Chunk's propositions:
        {' '.join(chunk['propositions'])}

        Current chunk summary:
        {chunk['summary']}

        Only respond with the new chunk summary, nothing else.
        """
        return self._make_api_call(prompt)

    def _update_chunk_title(self, chunk):
        prompt = f"""
        You are the steward of a group of chunks which represent groups of sentences that talk about a similar topic.
        A new proposition was just added to one of your chunks, you should generate a very brief updated chunk title which will inform viewers what a chunk group is about.
        A good title will say what the chunk is about.
        Your title should anticipate generalization. If you get a proposition about apples, generalize it to food.
        Or month, generalize it to "date and times".

        Chunk's propositions:
        {' '.join(chunk['propositions'])}

        Chunk summary:
        {chunk['summary']}

        Current chunk title:
        {chunk['title']}

        Only respond with the new chunk title, nothing else.
        """
        return self._make_api_call(prompt)

    def _get_new_chunk_summary(self, proposition):
        prompt = f"""
        You are the steward of a group of chunks which represent groups of sentences that talk about a similar topic.
        You should generate a very brief 1-sentence summary which will inform viewers what a chunk group is about.
        A good summary will say what the chunk is about, and give any clarifying instructions on what to add to the chunk.
        Your summaries should anticipate generalization. If you get a proposition about apples, generalize it to food.
        Or month, generalize it to "date and times".

        Determine the summary of the new chunk that this proposition will go into:
        {proposition}

        Only respond with the new chunk summary, nothing else.
        """
        return self._make_api_call(prompt)

    def _get_new_chunk_title(self, summary):
        prompt = f"""
        You are the steward of a group of chunks which represent groups of sentences that talk about a similar topic.
        You should generate a very brief few word chunk title which will inform viewers what a chunk group is about.
        A good chunk title is brief but encompasses what the chunk is about.
        Your titles should anticipate generalization. If you get a proposition about apples, generalize it to food.
        Or month, generalize it to "date and times".... Determine the title of the chunk that this summary belongs to:
        {summary}

        Only respond with the new chunk title, nothing else.
        """
        return self._make_api_call(prompt)

    def _create_new_chunk(self, proposition):
        new_chunk_id = str(uuid.uuid4())[:self.id_truncate_limit]
        new_chunk_summary = self._get_new_chunk_summary(proposition)
        new_chunk_title = self._get_new_chunk_title(new_chunk_summary)
        self.chunks[new_chunk_id] = {
            'chunk_id': new_chunk_id,
            'propositions': [proposition],
            'title': new_chunk_title,
            'summary': new_chunk_summary,
            'chunk_index': len(self.chunks)
        }
        if self.print_logging:
            print(f"Created new chunk ({new_chunk_id}): {new_chunk_title}")

    def get_chunk_outline(self):
        chunk_outline = ""
        for chunk_id, chunk in self.chunks.items():
            single_chunk_string = f"""Chunk ID: {chunk['chunk_id']}\nChunk Name: {chunk['title']}\nChunk Summary: {chunk['summary']}\n\n"""
            chunk_outline += single_chunk_string
        return chunk_outline

    def _find_relevant_chunk(self, proposition):
        current_chunk_outline = self.get_chunk_outline()
        prompt = f"""
        Determine whether or not the "Proposition" should belong to any of the existing chunks.
        A proposition should belong to a chunk if their meaning, direction, or intention are similar.
        The goal is to group similar propositions and chunks.
        If you think a proposition should be joined with a chunk, return the chunk id.
        If you do not think an item should be joined with an existing chunk, just return "No chunks"

        Current Chunks:
        --Start of current chunks--
        {current_chunk_outline}
        --End of current chunks--

        Determine if the following statement should belong to one of the chunks outlined:
        {proposition}

        Only respond with the chunk id or "No chunks", nothing else.
        """
        response_text = self._make_api_call(prompt)
        chunk_found = response_text.strip()

        if chunk_found != "No chunks" and len(chunk_found) == self.id_truncate_limit:
            return chunk_found
        return None

    def get_chunks(self, get_type='dict'):
        if get_type == 'dict':
            return self.chunks
        if get_type == 'list_of_strings':
            chunks = []
            for chunk_id, chunk in self.chunks.items():
                chunks.append(" ".join([x for x in chunk['propositions']]))
            return chunks

    def pretty_print_chunks(self):
        print(f"\nYou have {len(self.chunks)} chunks\n")
        for chunk_id, chunk in self.chunks.items():
            print(f"Chunk #{chunk['chunk_index']}")
            print(f"Chunk ID: {chunk_id}")
            print(f"Summary: {chunk['summary']}")
            print(f"Propositions:")
            for prop in chunk['propositions']:
                print(f" -{prop}")
            print("\n\n")

    def pretty_print_chunk_outline(self):
        print("Chunk Outline\n")
        print(self.get_chunk_outline())

    def chunk(self, text: str) -> None:
        """
        Splits the input text into semantic chunks and adds them to the chunks.
        """


        text_splitter = RecursiveCharacterTextSplitter(chunk_size =300 , chunk_overlap=0) # ["\n\n", "\n", " ", ""] 65,450
        documents=text_splitter.create_documents([text])
        document_strings = [doc.page_content for doc in documents]
        
        for i in document_strings:
            print(i)
        self.add_propositions(document_strings)
        print(self.pretty_print_chunk_outline())
        return self.chunks
    


if __name__ == "__main__":
    ac = AgenticChunker()
    """propositions = [
        'The month is October.',
        'The year is 2023.',
        "One of the most important things that I didn't understand about the world as a child was the degree to which the returns for performance are superlinear.",
        'Teachers and coaches implicitly told us that the returns were linear.',
        "I heard a thousand times that 'You get out what you put in.'",
        "The cat sat on the mat.",
        "The dog barked loudly.",
        "The bird flew high in the sky.",
        "The sun shone brightly.",
        "The moon glowed softly.",
        "Stars twinkled in the night.",
        "Rain fell gently on the ground.",
        "Wind whispered through the trees.",
        "Waves crashed against the shore.",
        "Fire crackled in the hearth.",
        "Smoke curled into the air.",
        "Shadows danced in the darkness.",
        "Silence filled the room.",
        "Time passed slowly.",
        "Memories lingered in the mind.",
        "Dreams floated through the night.",
        "Hopes soared towards the future.",
        "Fears lurked in the shadows.",
        "Love bloomed in the heart.",
        "Tears welled up in the eyes.",
        "Laughter echoed in the halls.",
        "Smiles brightened the faces.",
        "Joy filled the air.",
        "Sadness weighed down the soul.",
        "Anger flared in the spirit.",
        "Peace settled over the land.",
        "Chaos reigned in the streets.",
        "Order emerged from the confusion.",
        "Justice prevailed in the end."
    ]"""
    text="""A police station (sometimes called a "station house" or just "house") is a building which serves
    to accommodate police officers and other members of police staff. Police stations typically contain offices
    and accommodation for personnel and vehicles, along with locker rooms, temporary holding cells and interview/interrogation rooms.
    A smartphone is a mobile device that combines the functionality of a traditional mobile phone with advanced computing capabilities. 
    It typically has a touchscreen interface, allowing users to access a wide range of applications and services, such as web browsing, 
    email, and social media, as well as multimedia playback and streaming. Smartphones have built-in cameras, GPS navigation, and support 
    for various communication methods, including voice calls, text messaging, and internet-based messaging apps. Smartphones are distinguished 
    from older-design feature phones by their more advanced hardware capabilities and extensive mobile operating systems, access to the internet, 
    business applications, mobile payments, and multimedia functionality, including music, video, gaming, radio, and television
"""
    ac.chunk(text)
    ac.pretty_print_chunks()
    ac.pretty_print_chunk_outline()
    print (ac.get_chunks(get_type='list_of_strings'))
    