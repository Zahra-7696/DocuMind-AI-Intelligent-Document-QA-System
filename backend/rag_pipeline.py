"""RAG pipeline for DocuMind AI.

This module handles:
- loading PDF files
- splitting them into chunks
- embedding chunks
- creating a vector store
- retrieving relevant chunks
- asking the LLM to answer using the retrieved context
"""

#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from pathlib import Path

from config.config import (
    OLLAMA_BASE_URL,
    OLLAMA_LLM_MODEL,
    OLLAMA_EMBED_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHROMA_PERSIST_DIR,
)


def get_llm() -> Ollama:
    """Create the local Ollama LLM object."""
    return Ollama(
        model=OLLAMA_LLM_MODEL,
        temperature=0.5,
        base_url=OLLAMA_BASE_URL,
    )


def get_embedding_model() -> OllamaEmbeddings:
    """Create the local Ollama embedding model object."""
    return OllamaEmbeddings(
        model=OLLAMA_EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )


def document_loader(file_path: str):
    """Load a PDF document into LangChain document objects."""
    loader = PyPDFLoader(file_path)
    return loader.load()


def text_splitter(data):
    """Split loaded documents into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    return splitter.split_documents(data)

def vector_database(chunks):
    """Create a Chroma vector store from chunks."""
    embedding_model = get_embedding_model()
    ids = [str(i) for i in range(len(chunks))]

    chroma_path = Path(CHROMA_PERSIST_DIR)
    chroma_path.mkdir(parents=True, exist_ok=True)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        ids=ids,
        persist_directory=str(chroma_path),
    )
    print("CHROMA_PERSIST_DIR =", CHROMA_PERSIST_DIR)
    return vectordb


def retriever(file_path: str):
    """Build a retriever from an uploaded PDF file."""
    loaded_docs = document_loader(file_path)
    chunks = text_splitter(loaded_docs)
    vectordb = vector_database(chunks)
    return vectordb.as_retriever(search_kwargs={"k": 3})


def retriever_qa(file_path: str, query: str) -> str:
    """Run a retrieval-based QA chain over the uploaded file."""
    if not file_path:
        return "Please upload a PDF file first."

    if not query or not query.strip():
        return "Please type a question first."

    llm = get_llm()
    retriever_obj = retriever(file_path)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever_obj,
        return_source_documents=False,
    )

    response = qa.invoke({"query": query})
    return response["result"]


def test_ollama_connection() -> str:
    """Small health check for the local Ollama setup."""
    try:
        embedding_model = get_embedding_model()
        vector = embedding_model.embed_query("test")
        llm = get_llm()
        reply = llm.invoke("Reply with exactly two words: connection works.")
        return (
            f"Ollama embedding OK. Vector length: {len(vector)}\n"
            f"LLM check: {reply}"
        )
    except Exception as exc:
        return (
            "Ollama connection failed.\n"
            "Make sure Ollama is running and the models are pulled.\n"
            f"Error: {exc}"
        )
