import re
import json
import asyncio
import os
from dotenv import load_dotenv
from async_google_trans_new import AsyncTranslator
from langdetect import detect
from flask import Blueprint, request, jsonify, Response
from main.utils import create_qa_chain
from main.followup import store_conversation_redis, generate_followups
from main.langgraph_flow import create_langgraph_flow, GraphState
from langchain_community.vectorstores import Pinecone as PineconeVectorStore  
from langchain_google_genai import GoogleGenerativeAIEmbeddings

main = Blueprint('main', __name__)

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def load_vector_store():
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = PineconeVectorStore.from_existing_index(index_name=PINECONE_INDEX_NAME, embedding=embeddings)
        print("[Vector Store] Loaded successfully")
        return vector_store
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        return None

vector_store = load_vector_store()
qa_chain = create_qa_chain(vector_store)


def make_links_clickable(text):
    """Ensure URLs are clickable by keeping them in plain text."""
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.sub(r'\1', text)


@main.route("/", methods=["GET"])
def home():
    """API home route."""
    return jsonify({"message": "Welcome to the CopBot Chat API!"})

users = {}

@main.route('/signin', methods=['POST'])
def signin():
    data = request.json
    user_id = data.get("userId")
    email = data.get("email")

    if not user_id or not email:
        return jsonify({"error": "Missing user ID or email"}), 400

    if user_id in users:
        # Already known user
        return jsonify({
            "message": "User signed in successfully (from memory)",
            "user_id": user_id,
        }), 200
    else:
        # New user (just tracked in memory, not DB)
        users[user_id] = email
        return jsonify({
            "message": "New user recognized (not stored permanently)",
            "user_id": user_id,
        }), 201


async def detect_language(text):
    """Detect the language of the input text."""
    try:
        return detect(text)
    except Exception:
        return "en"  

async def translate_text(text, target_lang="en"):
    """Translate text to the target language asynchronously."""
    translator = AsyncTranslator()
    return await translator.translate(text, target_lang)

langgraph_flow = create_langgraph_flow()  

@main.route("/query", methods=["POST"])
async def query_chatbot():
    """Process user queries and generate follow-up questions using LangGraph."""
    try:
        data = request.json
        user_id = data.get("user_id")
        email = data.get("email")
        query = data.get("query", "").strip()
        print("📥 Incoming:", data)

        if not user_id or not email:
            return jsonify({"error": "User ID and email are required"}), 400

        if query:
            try:
                language = await detect_language(query)
            except Exception as e:
                print(f"❌ Language detection failed: {e}")
                language = "en"

            query_translated = query
            if language in ["ta", "hi"]:
                query_translated = await translate_text(query, target_lang="en")

            try:
                result = langgraph_flow.invoke(GraphState({"query": query_translated, "email": email}))
                formatted_answer = make_links_clickable(result.get("response", "Sorry, I couldn't find an answer."))
            except Exception as e:
                print(f"⚠️ LangGraph failed, falling back to LangChain: {e}")
                result = qa_chain.invoke({"query": query_translated})
                formatted_answer = make_links_clickable(result["result"])

            if language in ["ta", "hi"]:
                formatted_answer = await translate_text(formatted_answer, target_lang=language)

            store_conversation_redis(email, query, formatted_answer)

            followups = generate_followups(email)
            if language in ["ta", "hi"]:
                followups = await asyncio.gather(*[translate_text(f, target_lang=language) for f in followups])

            return Response(
                json.dumps({
                    "email": email,
                    "answer": formatted_answer,
                    "followups": followups
                }, ensure_ascii=False),
                content_type="application/json; charset=utf-8"
            )

        return jsonify({"email": email})

    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return jsonify({"error": str(e)}), 500
