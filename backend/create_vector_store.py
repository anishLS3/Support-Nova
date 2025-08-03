# create_vector_store.py
import time
import os
import pickle
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, Docx2txtLoader, UnstructuredExcelLoader, TextLoader
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone,ServerlessSpec
from agentic_chunker import AgenticChunker

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def agentic_chunking(text: str) -> list:
    ac = AgenticChunker()
    ac.chunk(text)
    chunks=ac.get_chunks(get_type='list_of_strings')
    print(chunks)
    return chunks
     
def load_documents(directory: str) -> list:
    """ Load documents from the specified directory. """
    if not os.path.exists(directory):
        print(f"❌ Dataset directory does not exist: {directory}")
        return []
    
    supported_extensions = {".pdf", ".csv", ".docx", ".doc", ".xlsx", ".xls", ".txt"}
    documents = []
    
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
        return []
    
    return documents

def chunk_documents(documents: list) -> list:
    """ Chunk the loaded documents. """
    
    chunked_documents = []
    for doc in documents:
        agentic_chunker = AgenticChunker()  
        doc_chunks = agentic_chunker.chunk(doc.page_content)
        
        for chunk_id, chunk_data in doc_chunks.items():
            chunk_text = " ".join(chunk_data["propositions"])
            chunked_documents.append(Document(page_content=chunk_text, metadata=doc.metadata))

        time.sleep(60)
    return chunked_documents

def create_pinecone_vector_store(chunked_documents: list):
    """ Create Pinecone vector store from chunked documents. """
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        existing_indexes = pc.list_indexes().names()
        
        if PINECONE_INDEX_NAME not in existing_indexes:
            print(f"Creating new Pinecone index: {PINECONE_INDEX_NAME}")
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        while True:
            index_info = pc.describe_index(PINECONE_INDEX_NAME)
            if index_info.status["ready"]:
                break
        print(f"Pinecone index '{PINECONE_INDEX_NAME}' is ready.")
        
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = PineconeVectorStore.from_documents(
            documents=chunked_documents,
            embedding=embeddings,
            index_name=PINECONE_INDEX_NAME
        )
        print(f"Successfully added {len(chunked_documents)} documents to Pinecone.")
        
        return vector_store
    
    except Exception as e:
        print(f"Error creating Pinecone vector store: {e}")
        return None

def main():
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the dataset path relative to the script's directory
    dataset_path = os.path.join(script_directory, "Dataset")
    documents = load_documents(dataset_path)
    chunked_documents = chunk_documents(documents)
    vector_store = create_pinecone_vector_store(chunked_documents)

if __name__ == "__main__":
    main()


