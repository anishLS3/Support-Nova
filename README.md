# NOVA - Personalized Customer Support Chatbot for STAR Systems Pvt. Ltd.

## 🚨 Problem Statement:

Conventional customer support chatbots often suffer from fragmented functionality, poor context retention, and lack of adaptability across different user needs. They require users to manually switch between services or follow rigid pathways, which can be frustrating and inefficient.

---

## 🔍 Project Overview:

NOVA is a personalized, AI-powered customer support chatbot developed for STAR Systems India Pvt. Ltd. It delivers a **single intelligent chat interface** that dynamically adapts to user intent and context, eliminating the inefficiencies and limitations of traditional chatbots. Whether it's answering FAQs, scheduling appointments, or escalating issues, NOVA intelligently identifies user needs and seamlessly switches between tasks without explicit user commands.

---

## 💡 Motivation:

With STAR Systems offering diverse services and products, addressing support queries quickly and efficiently becomes crucial. Manual handling leads to delays and inconsistent experiences. NOVA aims to:
- Automate customer service tasks intelligently.
- Provide real-time, accurate, and context-aware support.
- Minimize the workload on human agents by reducing unnecessary escalations.
- Enable seamless task-switching within a unified interface.

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

##  Architecture Flowchart

![Architecture Diagram](https://gitlab.digilabs.ai/Project-X-Hackathon-2025/Project-X-Hackathon-2025-Level-2/Shaurya/-/blob/main/images/RagPipeLine.jpeg?ref_type=heads)

##  Agent Workflow

![Agent Workflow](https://gitlab.digilabs.ai/Project-X-Hackathon-2025/Project-X-Hackathon-2025-Level-2/Shaurya/-/blob/main/images/Agent_WorkFlow.jpeg?ref_type=heads)

##  Frontend Output Screenshots

![Home Page](https://gitlab.digilabs.ai/Project-X-Hackathon-2025/Project-X-Hackathon-2025-Level-2/Shaurya/-/blob/main/images/HomePage.jpeg?ref_type=heads)

![Chat Page](https://gitlab.digilabs.ai/Project-X-Hackathon-2025/Project-X-Hackathon-2025-Level-2/Shaurya/-/blob/main/images/ChatPage.jpeg?ref_type=heads)

![Chat Page 1](https://gitlab.digilabs.ai/Project-X-Hackathon-2025/Project-X-Hackathon-2025-Level-2/Shaurya/-/blob/main/images/Chat.png?ref_type=heads)

##  Future Improvements

- **Voice Interaction**: Enable voice-based chat for accessibility and hands-free support.

- **Analytics Dashboard**: Build admin-level dashboards for chat statistics, FAQ usage, and performance metrics.

- **Auto-feedback Mechanism**: Let users rate responses to train and optimize model behavior.
