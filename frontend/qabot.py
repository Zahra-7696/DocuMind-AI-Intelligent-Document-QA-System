"""Gradio web app for DocuMind AI.

It provides:
- a PDF upload input
- a question textbox
- an answer textbox
- a small system check button for local Ollama status
"""

import gradio as gr

from backend.rag_pipeline  import retriever_qa, test_ollama_connection
from config.config import GRADIO_HOST, GRADIO_PORT


def run_qa(file, query):
    """Wrapper used by Gradio."""
    return retriever_qa(file, query)


with gr.Blocks(title="DocuMind AI") as rag_application:
    gr.Markdown(
        """
        # DocuMind AI
        Upload a PDF document and ask a question.
        The system will search the document and answer using a local Ollama model.
        """
    )

    with gr.Row():
        file_input = gr.File(
            label="Upload PDF File",
            file_count="single",
            file_types=[".pdf"],
            type="filepath",
        )
        query_input = gr.Textbox(
            label="Input Query",
            lines=3,
            placeholder="Type your question here...",
        )

    answer_output = gr.Textbox(
        label="Answer",
        lines=10,
    )

    ask_button = gr.Button("Ask")
    ask_button.click(
        fn=run_qa,
        inputs=[file_input, query_input],
        outputs=answer_output,
    )

    gr.Markdown("## Local system check")
    system_output = gr.Textbox(label="Ollama status", lines=6)
    check_button = gr.Button("Check Ollama")
    check_button.click(
        fn=test_ollama_connection,
        inputs=[],
        outputs=system_output,
    )


if __name__ == "__main__":
    rag_application.launch(
        server_name=GRADIO_HOST,
        server_port=GRADIO_PORT,
        share= True
    )
