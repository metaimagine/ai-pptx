import json
import re

from office import PPT
from pptx import Presentation

from utils.llm import LLM
from utils.prompter import PromptLibrarian


class PptxGenerator:
    PPT_PARAM_PATTERN = r'\{(.*?)\}'
    MD_CODE_JSON_PATTERN = r'```json.*?\n(.*?)```'

    def __init__(self, save_path: str, template_path: str):
        self.save_path = save_path
        self.has_template = False
        if template_path:
            self.has_template = True
            self.template_path = template_path
            self.template_ppt = Presentation(template_path)
            self.template_params = self._extract_params_from_template()

    def _extract_params_from_template(self):
        """生成PPT文件"""
        # 注意提取参数时，需要把模板PPT中的<组合>都解锁，不然可能存在找不到文本框的情况
        template_params = {
            "first_slide": {
                "nos": [0],
                "params": []
            },
            "catalogue_slide": {
                "nos": [1],
                "params": []
            },
            "title_slide": {
                "nos": [2],
                "params": []
            },
            "content_slide": {
                "nos": [3, 4, 5, 6, 7, 8],
                "params": []
            },
            "end_slide": {
                "nos": [-1],
                "params": []
            }
        }

        # PPT中同一页的{params}定义必须不同，避免混淆，不同页面不做要求
        for slide_name, slide_info in template_params.items():
            nos = slide_info["nos"]
            for n in nos:
                slide = self.template_ppt.slides[n]
                temp_params = []
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            for run in paragraph.runs:
                                matches = [match.group(1) for match in re.finditer(self.PPT_PARAM_PATTERN, run.text)]
                                temp_params.extend(matches)
                slide_info["params"].append(temp_params)
        return template_params

    def llm_generate_complate_content(self, llm: LLM, topic: str):
        """根据主题生成内容"""
        return llm.chat_once(
            prompt=PromptLibrarian.read(path="ppt.generate_content.v1").format(topic=topic),
            temperature=0.6
        )

    def llm_generate_ppt_content(self, llm: LLM, mina_content: str, author: str, now_date: str):
        """根据模板参数填充PPT内容"""
        output_format = json.dumps({
            "slide_list": [
                {"map_template_slide_no": 0, "params": ["p0_1", "p0_2", "p0_3"]},
                {"map_template_slide_no": 3, "params": ["p3_4", "p3_5", "p3_6"]},
                {"map_template_slide_no": 4, "params": ["p4_4", "p4_5", "p4_6"]},
                {"map_template_slide_no": "...", "params": ["..."]}
            ]
        })
        content = llm.chat_once(
            prompt=PromptLibrarian.read(path="ppt.generate_by_template.v1").format(
                template_params=self.template_params,
                output_format=output_format,
                mina_content=mina_content,
                author=author,
                now_date=now_date
            ),
            temperature=0.1
        )

        ppt_content = {}

        if content.startswith("```json"):
            matches = re.findall(self.MD_CODE_JSON_PATTERN, content, re.DOTALL)
            if matches:
                r = matches[0].replace("'", '"')
                ppt_content = json.loads(r)

        elif content.startswith("{"):
            ppt_content = json.loads(content)

        return ppt_content

    def generate_ppt_by_template(self, meta_info: dict, llm: LLM):
        """根据模板生成PPT"""
        topic = meta_info["topic"]
        author = meta_info["author"]
        now_date = meta_info["now_date"]

        # 注意：采用两步来生成PPT对应的内容，提高llm内容质量和字数，且后续更容易优化本身内容

        # 1. 单纯根据主题生成内容
        complate_content = self.llm_generate_complate_content(llm, topic)

        # 2. 根据模板填充PPT内容
        ppt_content = self.llm_generate_ppt_content(llm, complate_content, author, now_date)

        # 3. 根据模板新开ppt
        new_ppt = PPT().open(self.save_path, self.template_path)
        template_slides_count = len(new_ppt.slides)

        # 4. 在新ppt上，新增页并填充内容
        for p_slide_info in ppt_content['slide_list']:
            no = p_slide_info["map_template_slide_no"]
            params = p_slide_info["params"]
            new_slide = new_ppt.clone_slide(no, len(new_ppt.slides))

            for shape in new_slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            for match in re.finditer(self.PPT_PARAM_PATTERN, run.text):
                                if len(params) >= 1:
                                    p = params.pop(0)
                                    run.text = run.text.replace(match.group(0), str(p))
                                else:
                                    paragraph.text = '#blank#'

        # 5. 清空模板页
        for _ in range(template_slides_count): new_ppt.delete_slide(0)

        # 6. 保存PPT
        new_ppt.save()
