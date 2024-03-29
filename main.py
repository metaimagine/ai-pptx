import datetime
import json

from utils.llm import LLM
from utils.pptx_generator import PptxGenerator

with open('setting.json', 'r') as file:
    setting = json.load(file)


def main():
    llm = LLM(
        api_key=setting["llm"]["api_key"],
        base_url=setting["llm"]["base_url"],
        model_name=setting["llm"]["model_name"]
    )

    template_path = input('input template.pptx path: \n> ')  # "./ppt_template/beauty.pptx"
    save_path = input('input save path: \n> ')  # "output.pptx"

    while True:
        # 输入需求
        topic = input('input your topic: (`quiz` to exit)\n> ')
        if topic == 'quiz': break
        author = input('input author name: \n> ')
        gen = PptxGenerator(llm=llm, save_path=save_path, template_path=template_path)
        gen.generate(
            meta_info=dict(
                topic=topic, author=author, now_date=datetime.datetime.now().strftime("%Y%m%d")
            )
        )


if __name__ == '__main__':
    main()
