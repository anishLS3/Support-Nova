# NOVA – Personalized AI-Powered Customer Support Chatbot

## 🚨 Problem Statement:

Conventional customer support chatbots often suffer from fragmented functionality, poor context retention, and lack of adaptability across different user needs. They require users to manually switch between services or follow rigid pathways, which can be frustrating and inefficient.

---

## 🔍 Project Overview:

NOVA is an AI-powered, personalized customer support chatbot designed to deliver a unified, intelligent interface that understands user intent, retains context, and dynamically adapts to switch between tasks — such as handling FAQs, complaints, or appointment scheduling — without requiring explicit user commands.

---

## 💡 Key Objectives

- Automate customer support tasks with context-aware, real-time assistance
- Minimize human agent workload via smart escalation
- Enable dynamic task switching inside a single unified conversation flow
- Improve response accuracy with retrieval-augmented generation (RAG)

---

## 🏗 Architecture Overview:

### 🔧 Tech Stack

| Layer | Technology | Purpose |
|------|-------------|---------|
| **Frontend** | React.js | Real-time chat interface |
| **Backend** | Flask (Python) | API management and LLM integration |
| **AI/NLP** | LangChain, Gemini-2.0 Flash API | Intent detection, response generation |
| **Vector DB** | Pinecone | Semantic search for RAG |
| **Session Store** | Redis | Memory management and multi-turn dialogue |
| **Orchestration** | LangGraph | Agent routing and workflow control |
| **Notifications** | SMTP | Escalation email alerts to support team |

---

## 🧩 Core Components

### 1. **LangGraph (LangChain)**
- Orchestrates multi-agent workflows.
- Enables dynamic intent-based routing.
- Modular and scalable architecture.

### 2. **Gemini-2.0 Flash API**
- Performs intent classification.
- Generates intelligent, context-aware responses using RAG.

### 3. **RAG with Pinecone**
- Integrates semantic search with Google embeddings.
- Retrieves accurate knowledge chunks to ground responses.

### 4. **Agentic Chunking**
- Chunks data semantically to improve retrieval relevance.

### 5. **Redis + LangChain Memory**
- Tracks the last 3 user interactions.
- Maintains personalized conversation flow.

### 6. **Complaint & Escalation Agent**
- Gathers and validates complaint details.
- Escalates unresolved queries via email to human support.

### 7. **Intent Detection Agent**
- Classifies user queries into tasks (FAQ, complaint, etc.).
- Enables smooth task-switching within the chat interface.

---

## 🔐 Security and Configuration

- All sensitive keys and credentials are stored in a `.env` file.
- Separate configurations for development and production environments.
- SMTP integration for email notifications is secured using environment variables.

---

## ⚙️ Setup and Deployment

1. **Clone Repository**
```bash
git clone https://github.com/HariSabapaty/SupportNova.git
cd SupportNova
```

### 2. **Install Backend Requirements**
Navigate to the backend folder and install required Python packages:

```bash
cd backend
pip install -r requirements.txt
```
### 3. **Start Flask Backend**
Run the Flask server:

```bash
cd backend
python app.py
```
### 4. **Install Frontend Dependencies & Start**
Navigate to the frontend folder and start the React development server:

```bash
cd frontend
npm install
npm start
```
### 5. **Install Frontend Dependencies & Start**
Create a .env file in the root directory and populate it with the  environment variables

## 🧭 Architecture Flowchart

![Architecture Diagram](https://github.com/anishLS3/Support-Nova/blob/main/images/RagPipeLine.jpeg?raw=true)

## 🧠 Agent Workflow

![Agent Workflow](https://github.com/anishLS3/Support-Nova/blob/main/images/Agent_WorkFlow.jpeg?raw=true)

## 🖥️ Frontend Output Screenshots

![Home Page](https://github.com/anishLS3/Support-Nova/blob/main/images/HomePage.jpeg?raw=true)

##  Future Improvements

- **Voice Interaction**: Enable voice-based chat for accessibility and hands-free support.

- **Analytics Dashboard**: Build admin-level dashboards for chat statistics, FAQ usage, and performance metrics.

- **Auto-feedback Mechanism**: Let users rate responses to train and optimize model behavior.
