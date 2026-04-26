"""Gradio web app for DocuMind AI.

It provides two modes:
1. Local RAG using Ollama
2. AWS RAG using S3 + Bedrock
"""

import gradio as gr

from backend.rag_pipeline import retriever_qa, test_ollama_connection
from backend.aws_rag_pipeline import aws_retriever_qa, test_aws_bedrock_connection
from config.config import GRADIO_HOST, GRADIO_PORT


def run_local_qa(file, query):
    """Run local Ollama RAG."""
    return retriever_qa(file, query)


def run_aws_qa(file, query):
    """Run AWS Bedrock RAG."""
    return aws_retriever_qa(file, query)


with gr.Blocks(title="DocuMind AI") as rag_application:
    gr.Markdown(
        """
        # DocuMind AI

        Upload a PDF document and ask questions using either:

        - **Local mode:** Ollama + Chroma
        - **AWS mode:** S3 + Amazon Bedrock
        """
    )

    with gr.Tab("Local Ollama RAG"):
        gr.Markdown(
            """
            ## Local RAG Pipeline
            This mode uses local Ollama models for embeddings and answer generation.
            """
        )

        with gr.Row():
            local_file_input = gr.File(
                label="Upload PDF File",
                file_count="single",
                file_types=[".pdf"],
                type="filepath",
            )
            local_query_input = gr.Textbox(
                label="Input Query",
                lines=3,
                placeholder="Type your question here...",
            )

        local_answer_output = gr.Textbox(
            label="Local Ollama Answer",
            lines=10,
        )

        local_ask_button = gr.Button("Ask with Local Ollama")
        local_ask_button.click(
            fn=run_local_qa,
            inputs=[local_file_input, local_query_input],
            outputs=local_answer_output,
        )

        gr.Markdown("## Local system check")
        local_system_output = gr.Textbox(label="Ollama status", lines=6)
        local_check_button = gr.Button("Check Ollama")
        local_check_button.click(
            fn=test_ollama_connection,
            inputs=[],
            outputs=local_system_output,
        )

    with gr.Tab("AWS Bedrock RAG"):
        gr.Markdown(
            """
            ## AWS RAG Pipeline
            This mode uploads the PDF to **Amazon S3**, creates embeddings using
            **Amazon Titan Text Embeddings V2**, retrieves relevant chunks, and generates
            the final answer using **Amazon Nova Lite**.
            """
        )

        with gr.Row():
            aws_file_input = gr.File(
                label="Upload PDF File",
                file_count="single",
                file_types=[".pdf"],
                type="filepath",
            )
            aws_query_input = gr.Textbox(
                label="Input Query",
                lines=3,
                placeholder="Type your question here...",
            )

        aws_answer_output = gr.Textbox(
            label="AWS Bedrock Answer",
            lines=12,
        )

        aws_ask_button = gr.Button("Ask with AWS Bedrock")
        aws_ask_button.click(
            fn=run_aws_qa,
            inputs=[aws_file_input, aws_query_input],
            outputs=aws_answer_output,
        )

        gr.Markdown("## AWS system check")
        aws_system_output = gr.Textbox(label="AWS Bedrock status", lines=6)
        aws_check_button = gr.Button("Check AWS Bedrock")
        aws_check_button.click(
            fn=test_aws_bedrock_connection,
            inputs=[],
            outputs=aws_system_output,
        )


if __name__ == "__main__":
    rag_application.launch(
        server_name=GRADIO_HOST,
        server_port=GRADIO_PORT,
        share=True,
        #open http://127.0.0.1:7860
    )