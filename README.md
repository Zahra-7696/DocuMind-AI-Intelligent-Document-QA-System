# 🚀 DocuMind AI

## 📌 Overview
DocuMind AI is an end-to-end document question-answering system that enables users to upload PDF files and interact with their content using natural language queries. 
The system is built on a Retrieval-Augmented Generation (RAG) architecture, where document content is first processed and converted into vector embeddings using a local embedding model (Ollama). These embeddings are stored in a Chroma vector database, allowing efficient semantic search.
When a user submits a query, the system retrieves the most relevant document chunks and passes them, along with the query, to a local large language model (LLM) via Ollama. The model then generates a context-aware response grounded in the original document content.
LangChain is used to orchestrate the pipeline, connecting document loading, text splitting, embedding, retrieval, and response generation into a unified workflow. The system is exposed through a Gradio-based web interface for user interaction, and a FastAPI backend for integration with external systems.


## ⚙️ How It Works
The system follows a structured RAG pipeline:

1. Document Loading → Reads PDF using PyPDFLoader
2. Text Splitting → Breaks content into manageable chunks
3. Embedding Generation → Uses Ollama embedding model (mxbai-embed-large)
4. Vector Storage → Stores embeddings in Chroma DB
5. Retrieval → Finds most relevant chunks for the query
6. Answer Generation → Uses Ollama LLM (llama3.1:8b) to generate responses

🧱 Tech Stack
- LLM: Ollama (local models)
- Framework: LangChain
- Vector DB: Chroma
- Frontend: Gradio
- Backend API: FastAPI
- Containerization: Docker
- CI/CD: GitHub Actions, Jenkins
- Orchestration: Kubernetes
- Monitoring: Prometheus + Grafana

## 📂 Project Structure


```text
Github-QA-Bot-answer-PDF/
│
├── backend/
│   ├── __init__.py
│   ├── api.py
│   └── rag_pipeline.py
│
├── config/
│   ├── __init__.py
│   └── config.py
│
├── frontend/
│   ├── __init__.py
│   └── qabot.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── monitoring/
│   └── prometheus.yml
│
├── screenshots/
├── pdf-example/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── Jenkinsfile
├── documind-deployment.yaml
├── documind-service.yaml
│
├── requirements.txt
└── README.md

## 🧪 Local Setup
ollama pull mxbai-embed-large
ollama pull llama3.1:8b

pip install -r requirements.txt

python -m frontend.qabot

Open:
http://127.0.0.1:7860

## 🐳 run in Docker
docker build -t documind-ai .

docker run -p 7860:7860 -e GRADIO_HOST=0.0.0.0 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 documind-ai

## 🔌 API
uvicorn backend.api:app --reload --port 8000

http://127.0.0.1:8000/docs

## 📊 Monitoring
Prometheus: http://localhost:9091
Grafana: http://localhost:3001

## ☸️ Kubernetes Deployment
kubectl apply -f documind-deployment.yaml
kubectl apply -f documind-service.yaml

🔁 CI/CD Pipeline
GitHub Actions
Automatic build on push

## Jenkins
Docker build & deploy pipeline
Container lifecycle management

## 👩‍💻 Author
PhD in Computer Science with experience in machine learning, optimization, and applied AI systems. Contact: z.torabi.university@gmail.com