"""AWS Bedrock RAG pipeline for DocuMind AI.

This pipeline keeps the local Ollama version untouched.
It uses:
- PDF loading with PyPDFLoader
- LangChain text splitting
- Amazon Titan Embeddings V2
- simple cosine similarity retrieval
- Amazon Nova Lite for answer generation
- optional S3 upload for storing uploaded PDFs
"""

import json
import uuid
from typing import List, Tuple

import boto3
import numpy as np
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from config.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    BEDROCK_EMBED_MODEL,
    BEDROCK_LLM_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


s3_client = boto3.client("s3", region_name=AWS_REGION)
bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def upload_pdf_to_s3(file_path: str) -> str:
    """Upload PDF to S3 and return the S3 object key."""
    object_key = f"uploads/{uuid.uuid4()}.pdf"

    s3_client.upload_file(
        Filename=file_path,
        Bucket=S3_BUCKET_NAME,
        Key=object_key,
    )

    return object_key


def load_and_split_pdf(file_path: str):
    """Load PDF and split it into chunks."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    return splitter.split_documents(documents)


def get_bedrock_embedding(text: str) -> List[float]:
    """Generate embedding using Amazon Titan Text Embeddings V2."""
    body = {
        "inputText": text
    }

    response = bedrock_client.invoke_model(
        modelId=BEDROCK_EMBED_MODEL,
        body=json.dumps(body),
    )

    result = json.loads(response["body"].read())
    return result["embedding"]


def build_vector_index(chunks) -> Tuple[np.ndarray, List[str]]:
    """Create an in-memory vector index from PDF chunks."""
    texts = [chunk.page_content for chunk in chunks]
    embeddings = []

    for text in texts:
        embeddings.append(get_bedrock_embedding(text))

    return np.array(embeddings), texts


def cosine_similarity(query_vector, document_vectors):
    """Calculate cosine similarity."""
    query_vector = np.array(query_vector)

    similarities = np.dot(document_vectors, query_vector) / (
        np.linalg.norm(document_vectors, axis=1) * np.linalg.norm(query_vector)
    )

    return similarities


def retrieve_relevant_chunks(query: str, document_vectors, texts: List[str], k: int = 3) -> List[str]:
    """Retrieve top-k relevant chunks."""
    query_embedding = get_bedrock_embedding(query)
    similarities = cosine_similarity(query_embedding, document_vectors)

    top_indices = similarities.argsort()[-k:][::-1]
    return [texts[i] for i in top_indices]


def generate_answer_with_nova(query: str, context_chunks: List[str]) -> str:
    """Generate grounded answer using Amazon Nova Lite."""
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are DocuMind AI. Answer the user's question using only the context below.
If the answer is not available in the context, say: "I could not find this information in the uploaded document."

Context:
{context}

Question:
{query}
"""

    response = bedrock_client.converse(
        modelId=BEDROCK_LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
        inferenceConfig={
            "maxTokens": 500,
            "temperature": 0.2,
            "topP": 0.9,
        },
    )

    return response["output"]["message"]["content"][0]["text"]


def aws_retriever_qa(file_path: str, query: str) -> str:
    """Run full AWS Bedrock RAG pipeline."""
    if not file_path:
        return "Please upload a PDF file first."

    if not query or not query.strip():
        return "Please type a question first."

    try:
        s3_key = upload_pdf_to_s3(file_path)

        chunks = load_and_split_pdf(file_path)
        document_vectors, texts = build_vector_index(chunks)
        relevant_chunks = retrieve_relevant_chunks(query, document_vectors, texts)
        answer = generate_answer_with_nova(query, relevant_chunks)

        return f"{answer}\n\n[S3 file stored at: s3://{S3_BUCKET_NAME}/{s3_key}]"

    except Exception as exc:
        return f"AWS Bedrock pipeline failed:\n{exc}"


def test_aws_bedrock_connection() -> str:
    """Small health check for AWS Bedrock setup."""
    try:
        embedding = get_bedrock_embedding("connection test")

        response = bedrock_client.converse(
            modelId=BEDROCK_LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": "Reply with exactly two words: AWS works."}],
                }
            ],
            inferenceConfig={
                "maxTokens": 20,
                "temperature": 0.1,
            },
        )

        reply = response["output"]["message"]["content"][0]["text"]

        return (
            f"AWS Bedrock embedding OK. Vector length: {len(embedding)}\n"
            f"LLM check: {reply}"
        )

    except Exception as exc:
        return f"AWS Bedrock connection failed:\n{exc}"