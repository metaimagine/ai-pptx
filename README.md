# ai-pptx 

😆 Generate PPT by LLM follow your template.

📢 Not only use llm to generate ppt, but also according to your favorite ppt template. Just you need to simply change the template parameters.

## ShowCase
| Template                                 | Generated Slide                               |
|------------------------------------------|-------------------------------------------|
| <img src="./docs/imgs/template_ppt.png"> | <img src="./docs/imgs/generated_ppt.png"> |

## Installation

> python >= 3.10

1. Clone the [setting-example.json](./setting-example.json) and update your own llm api key `llm -> api_key`

```
$ cp setting-example.json setting.json
```

2. Install the dependencies

```
$ pip install -r requirements.txt
```

## Getting Started

### Run in Gradio

1. Run the [gradio_app.py](./gradio_app.py)

```
$ python gradio_app.py
```

2. Chat in terminal, input your template and content.

## How To Define Your Template

TODO write

## Features

- &#9745; Generate PPT by LLM
- &#9745; New PPT follow your template
- &#9745; Support gradio app
- &#9744; Generate all content by Agent

## License

Licensed under the [MIT](./LICENSE).

## Contact

See the homepage ;)