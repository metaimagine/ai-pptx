# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/25 16:44
@Author  : minglang.wu
@Email   : minglang.wu@tenclass.com
@File    : gradio_app.py
@Desc    :
"""
import datetime
import json

import gradio as gr
import random
import time
import logging

import pythoncom

from utils.pptx_generator import PptxGenerator

logger = logging.getLogger(__name__)
from utils.llm import LLM

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

with open('setting.json', 'r') as file:
    setting = json.load(file)

llm = LLM(
    api_key=setting["llm"]["api_key"],
    base_url=setting["llm"]["base_url"],
    model_name=setting["llm"]["model_name"]
)


def llm_chat(message: str, history: list, system_prompt: str, model_name: str, temperature: float):
    messages = []
    if system_prompt: messages.append({"role": "system", "content": system_prompt})
    for m in history:
        messages.append({"role": "user", "content": m[0]})
        messages.append({"role": "assistant", "content": m[1]})
    messages.append({"role": "user", "content": message})
    gen = llm.chat(messages, model_name=model_name, temperature=temperature)
    content = ""
    for partial_content in gen:
        content += partial_content
        yield content
    return "Done!"


def llm_chat_once(message: str, system_prompt: str, model_name: str, temperature: float):
    gen = llm.chat_once(prompt=message, system_prompt=system_prompt, model_name=model_name, temperature=temperature)
    content = ""
    for partial_content in gen:
        content += partial_content
    return content


def loop_chat_tab():
    with gr.Tab("多轮对话"):
        with gr.Row():
            with gr.Column(scale=3):
                system_prompt = gr.Textbox("You are helpful AI.", lines=4, label="📕 System Prompt")
            with gr.Column(scale=1):
                model_name = gr.Dropdown(["moonshot-v1-8k"], label="💻 Model Name", value="moonshot-v1-8k")
                temperature = gr.Slider(minimum=0.0, maximum=1.0, value=0.1, step=0.1, interactive=True,
                                        label="🌡 Temperature")

        with gr.Row():
            gr.ChatInterface(
                llm_chat, additional_inputs=[system_prompt, model_name, temperature]
            )


def once_chat_tab():
    with gr.Tab("单轮对话"):
        with gr.Row():
            with gr.Column(scale=4):
                system_prompt = gr.Textbox("You are helpful AI.",
                                           placeholder="input system prompt here!",
                                           label="📕 System Prompt")
                message = gr.Textbox("Hello, how are you?",
                                     placeholder="input your prompt here!",
                                     lines=6,
                                     label="📝 User Prompt")

            with gr.Column(scale=1):
                with gr.Row(): temperature = gr.Slider(minimum=0.0, maximum=1.0, value=0.1, step=0.1, interactive=True,
                                                       label="🌡 Temperature")
                with gr.Row():
                    with gr.Column(scale=1): model_name = gr.Dropdown(["moonshot-v1-8k"], label="💻 Model Name",
                                                                      value="moonshot-v1-8k")
                    with gr.Column(scale=1): chat_submit_btn = gr.Button(value="🚀 Send")

        result = gr.Textbox(label="💬 Response", lines=8)
        chat_submit_btn.click(llm_chat_once, inputs=[message, system_prompt, model_name, temperature], outputs=[result])


gen = PptxGenerator(llm, save_path="output.pptx", template_path="./ppt_template/beauty.pptx")


def init_or_reload_info(save_path: str, template_path: str):
    global gen
    gen = PptxGenerator(llm, save_path=save_path, template_path=template_path)


def generate_ppt_step1(topic: str):
    global gen
    if gen is None:
        return "Error!\n" \
               "Please input the path of template.pptx and save path, and click [Init/Reload] button!"
    return gen.llm_generate_online_content(topic)


def generate_ppt_step2(topic, author, company_name, online_content: str):
    global gen
    if gen is None:
        return "Error!\n" \
               "Please input the path of template.pptx and save path, and click [Init/Reload] button!"
    meta_info = {
        "topic": topic,
        "author": author,
        "company_name": company_name,
        "now_date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    generation_content = gen.llm_generate_content_slide_content(meta_info["topic"], online_content)
    gen.generate_ppt(meta_info, generation_content)


def ppt_generator_tab():
    global gen
    with gr.Tab("PPT生成"):
        with gr.Row():
            template_path = gr.Textbox("./ppt_template/beauty.pptx",
                                       label="PPT Template Path",
                                       placeholder='input template.pptx path',
                                       scale=3)
            save_path = gr.Textbox("output.pptx",
                                   label="PPT Save Path",
                                   placeholder='input save path',
                                   scale=3)
            init_or_reload_path_btn = gr.Button(value="🔄 Init/Reload", scale=1)
        with gr.Row():
            topic = gr.Textbox(label="Topic", placeholder='input your topic', scale=1)
            author = gr.Textbox(label="Author", placeholder='input author name', scale=1)
            company_name = gr.Textbox(label="Company Name", placeholder='input company name', scale=1)
        with gr.Row():
            # Step.1
            with gr.Column(scale=4):
                step1_btn = gr.Button(value="Step.1 生成大纲内容 👇")
                step1_output = gr.Code(language="json", interactive=True, lines=8, label="📝 Step.1 PPT大纲内容")
            # Step.2
            with gr.Column(scale=1):
                step2_btn = gr.Button(value="Step.2 生成完整内容 👇")

        init_or_reload_path_btn.click(init_or_reload_info, inputs=[save_path, template_path])
        step1_btn.click(generate_ppt_step1, inputs=[topic], outputs=[step1_output])
        step2_btn.click(generate_ppt_step2, inputs=[topic, author, company_name, step1_output])


with gr.Blocks(theme=gr.themes.Base()) as app:
    ppt_generator_tab()
    once_chat_tab()
    loop_chat_tab()

if __name__ == "__main__":
    app.launch(debug=True, show_error=True)
