import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from utils.memory import build_context, add_to_memory, get_memory_for_user
from main.utils import create_qa_chain1
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils.llm import get_llm
from utils.memory import get_memory_for_user

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME1 = os.getenv("PINECONE_INDEX_NAME1")  # FAQ index name
print(f"[FAQ Agent] PINECONE_INDEX_NAME1: {PINECONE_INDEX_NAME1}")

def load_vector_store1():
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = PineconeVectorStore.from_existing_index(
            index_name=PINECONE_INDEX_NAME1,
            embedding=embeddings
        )
        print("[FAQ Agent] Vector store loaded successfully.")
        return vector_store
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        return None

vector_store = load_vector_store1()
qa_chain = create_qa_chain1(vector_store)

def detect_intent_gemini(query: str, email: str) -> str:
    llm = get_llm()

    # Get last 3 messages to provide context
    memory = get_memory_for_user(email)
    history = "\n".join(memory[-3:]) if memory else ""

    prompt = f"""
                You are an intent classification assistant. Based on the conversation history and the user's latest message,
                determine the most appropriate intent from the following options:

                - complaint: The user is reporting a problem, issue, or dissatisfaction.
                - affirmation: The user is confirming they want further help (e.g., "yes", "please help", "sure", "I need it").
                - general: Any other kind of request (e.g., asking for info, FAQ-related, etc.)

                Conversation History:
                {history}

                User's Latest Message:
                {query}

                Return only one word: complaint, affirmation, or general.
                """

    response = llm.invoke(prompt)
    intent = response.content.strip().lower()

    if intent not in ["complaint", "affirmation", "general"]:
        return "general"  # fallback intent

    return intent

def get_faq_agent():
    def invoke(payload):
        query = payload.get("query")
        email = payload.get("email")

        print(f"[FAQ Agent] Query: {query} | Email: {email}")
        contextual_query = build_context(email, query)
        result = qa_chain.invoke({"query": contextual_query})
        response_text = result["result"]

        add_to_memory(email, query, response_text)

        intent = detect_intent_gemini(query, email)
        print(f"[FAQ Agent] Detected intent: {intent}")

        memory = get_memory_for_user(email)
        last_user_msg = memory[-1].split("User:")[-1].strip().lower() if memory else ""

        if intent == "complaint":
            followup = "Would you like further assistance from our customer care team?"
            add_to_memory(email, query, followup)
            return {
                "result": f"{response_text}\n\n{followup}",
                "intent": intent,
                "escalate": False
            }

        # Case 2: Affirmation received after a previous complaint - escalate
        elif intent == "affirmation" and any("complaint" in detect_intent_gemini(msg.split("User:")[-1], email) for msg in memory[-3:]):
            return {
                "result": "Okay, I will connect you with our customer care team for further assistance with your issue. Please wait while I transfer you.",
                "intent": intent,
                "escalate": True,
                "query": "The user confirmed they need support. Please proceed with escalation."
            }

        # Case 3: General inquiries (no escalation)
        return {
            "result": response_text,
            "intent": intent,
            "escalate": False
        }

    return RunnableLambda(invoke)
