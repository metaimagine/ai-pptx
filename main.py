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

    template_path = input('input template.pptx path: ')  # "./ppt_template/beauty.pptx"
    save_path = input('input save path: ')  # "output.pptx"

    while True:
        # 输入需求
        topic = input('input your topic: (`quiz` to exit)')
        if topic == 'quiz': break
        author = input('input author name: ')
        gen = PptxGenerator(save_path=save_path, template_path=template_path)
        gen.generate_ppt_by_template(
            meta_info=dict(topic=topic, author=author, now_date=datetime.datetime.now().strftime("%Y%m%d")),
            llm=llm
        )


if __name__ == '__main__':
    main()
