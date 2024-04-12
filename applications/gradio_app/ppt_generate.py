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
from config import config

from utils.pptx_generator import PptxGenerator

logger = logging.getLogger(__name__)
gen = PptxGenerator(
    config.llm, save_path="output.pptx", template_path="./ppt_template/beauty.pptx"
)


def init_or_reload_info(save_path: str, template_path: str):
    global gen
    gen = PptxGenerator(config.llm, save_path=save_path, template_path=template_path)


def generate_ppt_step1(topic: str):
    global gen
    if gen is None:
        return (
            "Error!\n"
            "Please input the path of template.pptx and save path, and click [Init/Reload] button!"
        )
    return gen.llm_generate_online_content(topic)


def generate_ppt_step2(topic, author, company_name, online_content: str):
    global gen
    if gen is None:
        return (
            "Error!\n"
            "Please input the path of template.pptx and save path, and click [Init/Reload] button!"
        )
    meta_info = {
        "topic": topic,
        "author": author,
        "company_name": company_name,
        "now_date": datetime.datetime.now().strftime("%Y-%m-%d"),
    }
    generation_content = gen.llm_generate_content_slide_content(
        meta_info["topic"], online_content
    )
    gen.generate_ppt(meta_info, generation_content)


def ppt_generator_tab():
    global gen
    with gr.Tab("PPT生成"):
        with gr.Row():
            template_path = gr.Textbox(
                "./ppt_template/beauty.pptx",
                label="PPT Template Path",
                placeholder="input template.pptx path",
                scale=3,
            )
            save_path = gr.Textbox(
                "output.pptx",
                label="PPT Save Path",
                placeholder="input save path",
                scale=3,
            )
            init_or_reload_path_btn = gr.Button(value="🔄 Init/Reload", scale=1)
        with gr.Row():
            topic = gr.Textbox(label="Topic", placeholder="input your topic", scale=1)
            author = gr.Textbox(
                label="Author", placeholder="input author name", scale=1
            )
            company_name = gr.Textbox(
                label="Company Name", placeholder="input company name", scale=1
            )
        with gr.Row():
            # Step.1
            with gr.Column(scale=1):
                step1_btn = gr.Button(value="Step.1 生成大纲内容 👇")
                step1_output = gr.Code(
                    language="json",
                    interactive=True,
                    lines=8,
                    label="📝 Step.1 PPT大纲内容",
                )
            # Step.2
            with gr.Column(scale=1):
                step2_btn = gr.Button(value="Step.2 生成完整内容 👇")
                # Step.3

        init_or_reload_path_btn.click(
            init_or_reload_info, inputs=[save_path, template_path]
        )
        step1_btn.click(generate_ppt_step1, inputs=[topic], outputs=[step1_output])
        step2_btn.click(
            generate_ppt_step2, inputs=[topic, author, company_name, step1_output]
        )
