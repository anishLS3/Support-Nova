import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",  
        google_api_key=api_key,
        temperature=0.5  
    )
