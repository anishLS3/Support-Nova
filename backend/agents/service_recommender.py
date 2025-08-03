import os
from dotenv import load_dotenv
from main.utils import create_qa_chain
from utils.memory import build_context, add_to_memory
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnableLambda

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def load_vector_store():
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = PineconeVectorStore.from_existing_index(
            index_name=PINECONE_INDEX_NAME,
            embedding=embeddings
        )
        print("[Vector Store] Loaded successfully")
        return vector_store
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        return None


vector_store = load_vector_store()
qa_chain = create_qa_chain(vector_store)  
print(f"[DEBUG] QA Chain type: {type(qa_chain)}")

def get_service_recommender_agent():
    # Set up vector store and chain
    vector_store = load_vector_store()
    qa_chain = create_qa_chain(vector_store)
    print(f"[DEBUG] QA Chain type: {type(qa_chain)}")

    # Define the agent logic
    def invoke(payload):
        query = payload["query"]
        email = payload["email"]
        contextual_query = build_context(email, query)
        result = qa_chain.invoke({"query": contextual_query})
        response_text = result["result"]
        add_to_memory(email, query, response_text)
        if response_text.lower().startswith("bot:"):
            response_text = response_text[4:].strip()
        
        return {"result": response_text}

    # Wrap with Runnable
    return RunnableLambda(invoke)




