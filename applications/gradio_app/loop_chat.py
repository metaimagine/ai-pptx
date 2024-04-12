
import gradio as gr
from config import config

def llm_chat(
    message: str, history: list, system_prompt: str, model_name: str, temperature: float
):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for m in history:
        messages.append({"role": "user", "content": m[0]})
        messages.append({"role": "assistant", "content": m[1]})
    messages.append({"role": "user", "content": message})
    gen = config.llm.chat(messages, model_name=model_name, temperature=temperature)
    content = ""
    for partial_content in gen:
        content += partial_content
        yield content
    return "Done!"

def loop_chat_tab():
    with gr.Tab("多轮对话"):
        with gr.Row():
            with gr.Column(scale=3):
                system_prompt = gr.Textbox(
                    "You are helpful AI.", lines=4, label="📕 System Prompt"
                )
            with gr.Column(scale=1):
                model_name = gr.Dropdown(
                    ["moonshot-v1-8k"], label="💻 Model Name", value="moonshot-v1-8k"
                )
                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.1,
                    step=0.1,
                    interactive=True,
                    label="🌡 Temperature",
                )

        with gr.Row():
            gr.ChatInterface(
                llm_chat, additional_inputs=[system_prompt, model_name, temperature]
            )
