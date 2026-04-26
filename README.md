# 🚀 DocuMind AI  
⚡ Hybrid RAG System: Ollama (Local LLM) + AWS Bedrock (Cloud AI)

## 📌 Overview

DocuMind AI is an end-to-end document question-answering system that enables users to upload PDF files and interact with their content using natural language queries.
The system is built on a Retrieval-Augmented Generation (RAG) architecture, where document content is first processed and converted into vector embeddings using a local embedding model (Ollama). These embeddings are stored in a Chroma vector database, allowing efficient semantic search.
When a user submits a query, the system retrieves the most relevant document chunks and passes them, along with the query, to a local large language model (LLM) via Ollama. The model then generates a context-aware response grounded in the original document content.
LangChain is used to orchestrate the pipeline, connecting document loading, text splitting, embedding, retrieval, and response generation into a unified workflow. The system is exposed through a Gradio-based web interface for user interaction, and a FastAPI backend for integration with external systems.

In addition to the local Ollama-based pipeline, DocuMind AI now includes an AWS-powered RAG pipeline. This mode uploads PDF files to Amazon S3, generates vector embeddings using Amazon Titan Text Embeddings V2 through Amazon Bedrock, retrieves the most relevant chunks using semantic similarity, and generates grounded answers using Amazon Nova Lite. This extension allows the project to demonstrate both local LLM deployment and cloud-based AI integration using practical AWS services.

## ⚙️ How It Works

The local system based on the RAG pipeline with OLLAMA:

1. Document Loading → Reads PDF using PyPDFLoader
2. Text Splitting → Breaks content into manageable chunks
3. Embedding Generation → Uses Ollama embedding model (mxbai-embed-large)
4. Vector Storage → Stores embeddings in Chroma DB
5. Retrieval → Finds most relevant chunks for the query
6. Answer Generation → Uses Ollama LLM (llama3.1:8b) to generate responses



The AWS RAG pipeline follows a cloud-integrated workflow:

1. PDF Upload → Uploads the selected PDF file to Amazon S3
2. Document Loading → Reads PDF content using PyPDFLoader
3. Text Splitting → Breaks document content into manageable chunks
4. AWS Embedding Generation → Uses Amazon Titan Text Embeddings V2 through Amazon Bedrock
5. Vector Retrieval → Computes semantic similarity and retrieves the most relevant chunks
6. AWS Answer Generation → Uses Amazon Nova Lite through Amazon Bedrock to generate grounded responses
7. Result Display → Shows the answer in the Gradio interface and returns the S3 storage location

## 🧱 Tech Stack

* LLM: Ollama (local models)
* Cloud LLM: Amazon Nova Lite via Amazon Bedrock
* Embedding Model: Ollama embedding model (mxbai-embed-large)
* Cloud Embedding Model: Amazon Titan Text Embeddings V2 via Amazon Bedrock
* Cloud Storage: Amazon S3
* AWS SDK: Boto3
* Framework: LangChain
* Vector DB: Chroma
* Frontend: Gradio
* Backend API: FastAPI
* Containerization: Docker
* CI/CD: GitHub Actions, Jenkins
* Orchestration: Kubernetes
* Monitoring: Prometheus + Grafana

## 📂 Project Structure

```text
Github-QA-Bot-answer-PDF/
│
├── backend/
│   ├── \_\_init\_\_.py
│   ├── api.py
│   ├── aws\_rag\_pipeline.py
│   └── rag\_pipeline.py
│
├── config/
│   ├── \_\_init\_\_.py
│   └── config.py
│
├── frontend/
│   ├── \_\_init\_\_.py
│   └── qabot.py
│
├── AWS-Connection-Tests/
│   ├── test\_presigned\_upload.py
│   ├── test\_embedding.py
│   └── test\_llm.py
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
```

## 🧪 Local Setup

```bash
ollama pull mxbai-embed-large
ollama pull llama3.1:8b

pip install -r requirements.txt

python -m frontend.qabot
```

Open:
http://127.0.0.1:7860

## ☁️ AWS Setup

Before running the AWS Bedrock RAG mode, configure AWS access locally.

```bash
aws configure
```

Enter:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name: us-east-1
Default output format: json
```

Create a private S3 bucket for uploaded PDFs:

```text
documind-ai-zahra-pdf-storage
```

Recommended S3 settings:

```text
Region: us-east-1
Block all public access: ON
Object ownership: ACLs disabled
Bucket versioning: OFF
Default encryption: SSE-S3
```

Test AWS identity:

```bash
aws sts get-caller-identity
```

Test S3 upload:

```bash
aws s3 cp ".\\pdf-example\\test.pdf" "s3://documind-ai-zahra-pdf-storage/uploads/test.pdf" --region us-east-1
aws s3 ls "s3://documind-ai-zahra-pdf-storage/uploads/" --region us-east-1
```

If the `aws` command opens a Windows app-selection window, use the full AWS CLI executable path:

```bash
"C:\\Program Files\\Amazon\\AWSCLIV2\\aws.exe" s3 cp ".\\pdf-example\\test.pdf" "s3://documind-ai-zahra-pdf-storage/uploads/test.pdf" --region us-east-1
```

## 🤖 AWS Bedrock RAG Mode

The AWS mode uses:

```text
Amazon S3 → PDF storage
Amazon Titan Text Embeddings V2 → embedding generation
Amazon Nova Lite → answer generation
Boto3 → AWS service integration
Gradio → user interface
```

Run the application:

```bash
python -m frontend.qabot
```

Open:

```text
http://127.0.0.1:7860
```

Then select:

```text
AWS Bedrock RAG
```

Use the AWS system check button to verify:

```text
AWS Bedrock embedding OK. Vector length: 1024
LLM check: AWS works.
```

## 🐳 Run in Docker

```bash
docker build -t documind-ai .

docker run -p 7860:7860 \\
  -e GRADIO\_HOST=0.0.0.0 \\
  -e OLLAMA\_BASE\_URL=http://host.docker.internal:11434 \\
  -e AWS\_REGION=us-east-1 \\
  -e S3\_BUCKET\_NAME=documind-ai-zahra-pdf-storage \\
  documind-ai
```

## 🔌 API

```bash
uvicorn backend.api:app --reload --port 8000
```

http://127.0.0.1:8000/docs

## 📊 Monitoring

Prometheus: http://localhost:9091  
Grafana: http://localhost:3001

## ☸️ Kubernetes Deployment

```bash
kubectl apply -f documind-deployment.yaml
kubectl apply -f documind-service.yaml
```

## 🔁 CI/CD Pipeline

### GitHub Actions

Automatic build on push

### Jenkins

Docker build \& deploy pipeline  
Container lifecycle management

## 📸 Screenshots

The project includes screenshots showing both RAG modes:

```text
Local Ollama RAG
AWS Bedrock RAG
```

These screenshots demonstrate that the application can answer document-based questions using both a local LLM pipeline and an AWS Bedrock-powered cloud pipeline.

## 👩‍💻 Author

PhD in Computer Science with experience in machine learning, optimization, and applied AI systems.  
Contact: z.torabi.university@gmail.com

