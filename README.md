# ai-pptx

Generate PPT by LLM follow your template.

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

1. Run the [main.py](./main.py)

```
$ python main.py
```

2. Chat with llm in terminal, input your template and content.

## Features

- &#9745; Generate PPT by LLM.
- &#9744; New PPT follow your template.
- &#9744; Support gradio app.

## Inspiration

[aippt](https://github.com/owenliang/aippt/tree/main)

[reveal.js](https://github.com/hakimel/reveal.js)

## License

Licensed under the [MIT](./LICENSE).
