from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter
import gradio as gr
from applications import gradio_app
import logging
import os
from config import config

logger = logging.getLogger(__name__)
app = FastAPI()

static_path = "./utils/revealjs/reveal_src"
templates_path = "./applications/templates"

templates = Jinja2Templates(directory=templates_path)

app.mount("/presentation/static", StaticFiles(directory=static_path), name="static")


@app.get("/presentation/{pid}")
def home(pid, request: Request):
    cache_path = os.path.join(os.getcwd(), f"{config.cache_folder}/{pid}.md")
    with open(cache_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("\n\n", "\n---\n")

    logger.info(content)

    data = {
        "content": content,
        "request": request
    }
    return templates.TemplateResponse("index.html", data)


# bind gradio
app = gr.mount_gradio_app(app, gradio_app.current_app, path="/gradio")
