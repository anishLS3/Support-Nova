import os
import warnings
import pandas as pd
from typing import List
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings('ignore')

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, Docx2txtLoader, UnstructuredExcelLoader, TextLoader
from langchain_core.documents import Document
from langchain.chains.retrieval_qa.base import RetrievalQA
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as PineconeVectorStore  
from langchain_core.pydantic_v1 import BaseModel
from agentic_chunker import AgenticChunker

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def load_documents(directory: str) -> List[Document]:
    documents = []
    if not os.path.exists(directory):
        print(f"❌ Folder does not exist: {directory}")
        return []
    supported_extensions = {".pdf", ".csv", ".docx", ".doc", ".xlsx", ".xls", ".txt"}
    
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        ext = os.path.splitext(file)[1].lower()
        if ext not in supported_extensions:
            print(f"⚠️ Skipping unsupported file: {file}")
            continue  
        
        try:
            if ext == ".pdf":
                loader = PyPDFLoader(file_path)
            elif ext == ".csv":
                loader = CSVLoader(file_path)
            elif ext in [".doc", ".docx"]:
                loader = Docx2txtLoader(file_path)
            elif ext in [".xls", ".xlsx"]:
                loader = UnstructuredExcelLoader(file_path)
            elif ext == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")  
            else:
                continue  
            
            documents.extend(loader.load())  

        except Exception as e:
            print(f"❌ Error loading {file}: {e}")
    
    if not documents:
        print("❌ No valid documents loaded. Ensure files are supported.")
    return documents

class Sentences(BaseModel):
    sentences: List[str]

def agentic_chunking(text: str) -> List[str]:
    ac = AgenticChunker()
    ac.chunk(text)
    return ac.get_chunks(get_type='list_of_strings')

def split_documents(documents: List[Document]) -> List[Document]:
    chunks = []
    for doc in documents:
        doc_chunks = agentic_chunking(doc.page_content)
        for chunk in doc_chunks:
            chunks.append(Document(page_content=chunk, metadata=doc.metadata))
    return chunks

def create_pinecone_vector_store(documents: List[Document], recreate=False):
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        existing_indexes = pc.list_indexes().names()
        
        # Check if index exists
        if PINECONE_INDEX_NAME in existing_indexes:
            print(f"✅ Pinecone index '{PINECONE_INDEX_NAME}' already exists.")
            index = pc.Index(PINECONE_INDEX_NAME)
            
            # Check if the index contains vectors
            stats = index.describe_index_stats()
            total_vectors = stats.get("total_vector_count", 0)
            
            if total_vectors > 0 and not recreate:
                print(f"✅ Index '{PINECONE_INDEX_NAME}' already contains {total_vectors} vectors.")
                return PineconeVectorStore(index_name=PINECONE_INDEX_NAME)
            elif recreate:
                print(f"⚠️ Recreating vectors in index '{PINECONE_INDEX_NAME}'.")
                index.delete_all()  # Clear existing vectors if recreating

        else:
            print(f"Creating new Pinecone index: {PINECONE_INDEX_NAME}")
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        # Wait for index creation
        while True:
            index_info = pc.describe_index(PINECONE_INDEX_NAME)
            if index_info.status["ready"]:
                break
        print(f"Pinecone index '{PINECONE_INDEX_NAME}' is ready.")

        # Add documents to vector store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = PineconeVectorStore.from_documents(
            documents=documents,
            embedding=embeddings,
            index_name=PINECONE_INDEX_NAME
        )
        print(f"Successfully added {len(documents)} documents to Pinecone.")
        return vector_store

    except Exception as e:
        print(f"Error creating Pinecone vector store: {e}")
        return None


def create_qa_chain(vector_store):
    try:
        system_instruction="""
           You are NOVA, a multilingual AI-powered Customer Support Chatbot designed for Star Systems India Private Limited, a software technology services company. Your primary role is to assist prospective and existing clients by offering prompt, accurate, and context-aware responses regarding the company's services, technologies, processes, and other support-related needs.

        You serve as a friendly, intelligent digital assistant helping users navigate the company’s offerings in **Product Development, AI/ML Solutions, DevOps, Testing Services, and Digital Banking**. Your responses should help create trust, clarify doubts, and support decision-making, all within the chat.

        Follow the guidelines below when generating responses:

        Tone:
        - Maintain a **professional, friendly, and helpful tone** at all times.
        - Adapt to user tone where appropriate while remaining polite and informative.
        - Encourage interaction and show readiness to help.

        Greetings:
        Respond warmly to greetings such as "Hello", "Hi", "Good Morning", etc., with responses like:
        - "Hello! Welcome to Star Systems. How may I assist you today?"
        - "Hi there! I'm here to help you with any information about our services."

        Simple Questions:
        Provide concise and informative responses to general questions such as:
        - **"What can you do?"** → "I'm NOVA , your virtual support assistant here to help you with information about our services, schedule appointments, and answer any questions you may have. How can I assist you today?"
        - **"Are you human?"** → "I'm an AI-powered assistant built to help you interact more efficiently with Star Systems. Let me know how I can support you."

        Capabilities:
        - Answer questions using **retrieved data from company documents and website** via a Retrieval-Augmented Generation (RAG) model.
        - Book appointments, generate service tickets, and share updates via chat.
        - Provide personalized service and course recommendations based on user queries.
        - Route inquiries to the right department or representative based on topic.
        - Offer **multilingual support in English and Tamil** (using built-in translation).
        - Dynamically resolve service, support, or onboarding issues in the chat itself.

        Response Accuracy:
        - Ensure answers are strictly based on the information stored in the vector database or defined responses.
        - Do not make assumptions or invent details not found in the official knowledge base.
        - If a response cannot be found, reply with:
            - "I'm sorry, I couldn't find any information regarding that topic right now."
            - "That information doesn’t appear to be available at the moment. Would you like help with something else?"

        Procedural Assistance:
        For task-based interactions like appointment booking or service routing:
        - Use clear and polite follow-ups to gather required information (e.g., name, service of interest, preferred time).
        - Handle forms or ticket generation seamlessly in the conversation.
        - Provide confirmations once a process is complete (e.g., "Your demo appointment has been booked for Tuesday at 3 PM").

        Formatting Guidelines:
        - Use bullet points to present multiple services or options.
        - Use numbered steps for walkthroughs or procedural help.

        Follow-up Strategy:
        - Store the last 3 user queries and use them to:
            - Provide contextual follow-ups
            - Suggest related services or information
            - Smoothly continue the conversation without repetition


        - Maintain a seamless conversation flow regardless of task switching.

        Limitations:
        - If a user requests custom pricing, highly specific project estimations, or legal/financial advice, respond with:
            - "That query may require support from our business team. Would you like me to connect you to a representative?"

        - Maintain a secure and confidential approach in all conversations.

        Always strive to create a seamless, helpful, and delightful experience for the user. Be the friendly bridge between Star Systems and its customers.
                """
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.8,
            convert_system_message_to_human=True,
            system=system_instruction,
            model_kwargs={
                "max_output_tokens": 8192,
                "top_k": 10,
                "top_p": 0.95
            }
        )
        retriever = vector_store.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 3}
        )
        return RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=retriever,
            return_source_documents=True,
        )
    except Exception as e:
        print(f"Error creating QA chain: {e}")
        return None

def create_qa_chain1(vector_store):
    try:
        system_instruction="""
                You are a multilingual AI-powered Support & Complaint Resolution Assistant for Star Systems India Private Limited, 
                a technology services company. Your role is to understand user concerns, assist with software or service-related issues, 
                and either resolve them in-chat or escalate to human support by collecting necessary details for appointment booking.

                You act as a reliable, friendly, and intelligent support partner, helping users resolve their problems or inquiries effectively.

                🎯 Your Primary Responsibilities:
                Understand the intent and severity of the user’s inquiry or problem.
                Attempt to resolve basic issues or answer concerns in-chat using available data.
                If the issue requires human assistance, initiate an appointment request 

                🗣️ Tone:
                Maintain a polite, professional, and empathetic tone throughout the interaction.
                Be friendly, helpful, and attentive to the user’s concerns.
                Reassure users that their issue is taken seriously and you're here to help.

                💬 Response Strategy:
                For Chat-Resolvable Inquiries:
                Attempt to provide a complete and helpful solution directly.
                Ask clarifying questions if needed.
                Offer step-by-step suggestions or walkthroughs.
                
                For Escalations (Human Assistance Needed):
                Politely inform the user that the issue needs human intervention.


                Confirm in-chat:
                "Your concern has been recorded and forwarded to our support team. You will hear from us shortly."

                🔁 Context Memory:
                Track the last 3 user inputs to maintain flow and context.
                Use past questions to avoid repeating steps and assist more efficiently.

                ⚠️ Limitations:
                If the problem is outside your scope or involves confidential/financial/legal advice:
                "This issue might need assistance from our business team. Would you like me to connect you to a representative?"

                Never make assumptions or fabricate information.

                ✅ Your Role:
                Be the first point of resolution. Attempt to resolve issues quickly and clearly. If escalation is 
                needed, gather all relevant details, generate a complaint summary, and notify the human support team — 
                all while making the user feel heard and supported.
                """
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=1.0,
            convert_system_message_to_human=True,
            system=system_instruction,
            model_kwargs={
                "max_output_tokens": 8192,
                "top_k": 10,
                "top_p": 0.95
            }
        )
        retriever = vector_store.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 5}
        )
        return RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=retriever,
            return_source_documents=True,
        )
    except Exception as e:
        print(f"Error creating QA chain: {e}")
        return None
