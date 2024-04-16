import gradio as gr

from .reveal_generate import reveal_generator_tab
from .ppt_generate import ppt_generator_tab
from .once_chat import once_chat_tab
from .loop_chat import loop_chat_tab

with gr.Blocks(theme=gr.themes.Base()) as app:
    reveal_generator_tab()
    ppt_generator_tab()
    once_chat_tab()
    loop_chat_tab()

current_app = app
