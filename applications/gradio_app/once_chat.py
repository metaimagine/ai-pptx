import gradio as gr
from config import config

def llm_chat_once(
    message: str, system_prompt: str, model_name: str, temperature: float
):
    gen = config.llm.chat_once(
        prompt=message,
        system_prompt=system_prompt,
        model_name=model_name,
        temperature=temperature,
    )
    content = ""
    for partial_content in gen:
        content += partial_content
    return content

def once_chat_tab():
    with gr.Tab("单轮对话"):
        with gr.Row():
            with gr.Column(scale=4):
                system_prompt = gr.Textbox(
                    "You are helpful AI.",
                    placeholder="input system prompt here!",
                    label="📕 System Prompt",
                )
                message = gr.Textbox(
                    "Hello, how are you?",
                    placeholder="input your prompt here!",
                    lines=6,
                    label="📝 User Prompt",
                )

            with gr.Column(scale=1):
                with gr.Row():
                    temperature = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.1,
                        step=0.1,
                        interactive=True,
                        label="🌡 Temperature",
                    )
                with gr.Row():
                    with gr.Column(scale=1):
                        model_name = gr.Dropdown(
                            ["moonshot-v1-8k"],
                            label="💻 Model Name",
                            value="moonshot-v1-8k",
                        )
                    with gr.Column(scale=1):
                        chat_submit_btn = gr.Button(value="🚀 Send")

        result = gr.Textbox(label="💬 Response", lines=8)
        chat_submit_btn.click(
            llm_chat_once,
            inputs=[message, system_prompt, model_name, temperature],
            outputs=[result],
        )
