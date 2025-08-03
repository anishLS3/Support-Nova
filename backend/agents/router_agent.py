import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY2")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# Define the prompt
router_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a smart routing agent that classifies customer queries into one of two categories:
     
- 'service': The user is asking about general features, how things work, product details, or seeking information.
  Examples:
    - "How do I migrate my app to the cloud?"
    - "What is the cost of your premium plan?"
    - "How does your API authentication work?"

- 'complaint': The user is reporting a problem, expressing dissatisfaction, facing a technical issue, or needing urgent help.
  Examples:
    - "My app crashed during migration."
    - "I'm facing errors when uploading files."
    - "The service is not working properly."

Classify the following query into either 'service' or 'complaint'. Respond with ONLY the word 'service' or 'complaint'. Do not explain.

Query:
"""),
    ("human", "{query}")
])

# Chain prompt + LLM
intent_classifier_chain = router_prompt | llm

# Final callable function
def classify_intent(query: str) -> str:
    try:
        result = intent_classifier_chain.invoke({"query": query})
        response = result.content.strip().lower()
        print(f"[Router Agent] Response: {response}")
        return response
    except Exception as e:
        print(f"❌ Intent classification failed: {e}")
        return "service"  # default fallback
