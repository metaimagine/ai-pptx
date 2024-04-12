"""
ref: https://github.com/webpro/reveal-md
npm install -g reveal-md

"""



from jinja2 import Environment, FileSystemLoader
import gradio as gr

def render_template(path):
    # 创建Jinja2环境
    env = Environment(loader=FileSystemLoader(path))

    # 加载模板文件
    t = env.get_template("index.html")

    # 准备要传递给模板的数据
    data = {
        "content": """
    ## Slide 1
        A paragraph with some text and a [link](https://hakim.se).
        ---
        ## Slide 2
        ---
        ## Slide 3
    """
    }

    # 使用数据渲染模板
    output = t.render(data)
    
    # 返回渲染后的HTML内容
    return output

static_path = "./utils/revealjs/reveal_src"
templates_path = "./utils/revealjs/templates"


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
app = FastAPI()

templates = Jinja2Templates(directory=templates_path)

app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/presentation/{pid}")
def home(pid, request: Request):
    print(f"pid: {pid}")
    data = {
        "content": """## Slide 1
A paragraph with some text and a [link](https://hakim.se).
---
## Slide 2
---
## Slide 3""",
        "request": request
    }
    return templates.TemplateResponse("index.html", data)

