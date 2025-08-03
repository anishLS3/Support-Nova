import redis
from pinecone import Pinecone
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve API keys and settings from .env
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY1 = os.getenv("GEMINI_API_KEY1")
REDIS_HOST = os.getenv("REDIS_CLOUD_HOST")
REDIS_PORT = int(os.getenv("REDIS_CLOUD_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_CLOUD_PASSWORD")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

print(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}")
# Initialize Redis Cloud connection
try:
    redis_client = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,  # Redis Cloud requires a password
        decode_responses=True
    )
    # Test connection
    redis_client.ping()
    print("✅ Successfully connected to Redis Cloud!")
except redis.ConnectionError as e:
    print(f"❌ Failed to connect to Redis Cloud: {e}")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

# Initialize Google Gemini API
genai.configure(api_key=GEMINI_API_KEY1)

def store_conversation_redis(email, query, response):
    """
    Stores the latest query and response in Redis.
    Maintains only the last three conversations per chat.
    """
    key = f"chat:{email}:history"

    # Retrieve existing conversations
    conversations = redis_client.lrange(key, 0, 2)  # Get up to last three
    conversations = [json.loads(conv) for conv in conversations]

    # Append new query-response pair
    conversations.append({"query": query, "response": response})

    # Keep only the last 3 conversations
    if len(conversations) > 3:
        conversations.pop(0)

    # Store back in Redis
    redis_client.delete(key)  # Clear old entries
    for conv in conversations:
        redis_client.rpush(key, json.dumps(conv))  # Push latest data

def get_last_three_conversations(email):
    """
    Retrieves the last three conversations from Redis.
    Ensures at least one conversation is available.
    """
    key = f"chat:{email}:history"
    conversations = redis_client.lrange(key, 0, 2)  # Get last three (max)

    if not conversations:
        return [{"query": "Hello", "response": "Hi! How can I help you?"}]  # Default if empty

    return [json.loads(conv) for conv in conversations]

def get_embedding(text):
    """
    Generates an embedding for a given text using Google Gemini.
    """
    embedding_model = "models/embedding-001"  # Correct model path
    response = genai.embed_content(model=embedding_model, content=text, task_type="retrieval_query")
    return response["embedding"]  # Extract the embedding from the response

def get_relevant_context(conversations):
    """
    Searches Pinecone for relevant context based on the last three queries.
    """
    context_list = []

    for conversation in conversations:
        query_embedding = get_embedding(conversation["query"])  # Convert query to vector
        results = index.query(vector=query_embedding, top_k=3, include_metadata=True)  # Fetch best matches

        for match in results["matches"]:
            context_list.append(match["metadata"]["text"])

    return context_list  # List of relevant contexts

def generate_followups(email):
    """
    Generates exactly three follow-up questions based on last queries and Pinecone knowledge.
    """
    # Retrieve last 3 conversations
    conversations = get_last_three_conversations(email)

    # Extract relevant context from Pinecone
    context_list = get_relevant_context(conversations)

    # Prepare prompt for LLM
    prompt = f"""
    You are an AI assistant that helps users by suggesting exactly three helpful follow-up questions they might consider asking next. These questions should guide the user toward resolving their issue more efficiently or exploring the topic further.

    Do not generate questions for the bot to ask — generate suggestions *for the user* to ask the bot next.

    The questions should:
    - Be relevant to the user's past queries and the provided knowledge
    - Be short, clear, and action-oriented
    - Feel natural and assist the user in continuing the conversation meaningfully

    **Last User Conversations:**
    {json.dumps(conversations, indent=2)}

    **Relevant Knowledge from the Database:**
    {json.dumps(context_list, indent=2)}

    Based on the above, generate exactly three follow-up *question suggestions for the user*.
    """

    # Call Gemini API
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    if response.candidates:
        followup_questions = response.candidates[0].content.parts[0].text.strip().split("\n")
    else:
        followup_questions = [
            "Can you provide more details?",
            "What specific aspect interests you?",
            "Do you need examples or further clarification?"
        ]

    return followup_questions[:3]  # Ensure exactly 3 follow-ups