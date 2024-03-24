# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/21 18:37
@Author  : minglang.wu
@Email   : minglang.wu@tenclass.com
@File    : prompt_manager.py
@Desc    :
"""
import json


class PromptManager:
    def __init__(self, d: str):
        self.prompt = d

    def json_format(self, output_format: dict):
        """按JSON格式输出"""
        output_format = json.dumps(output_format, ensure_ascii=True)
        self.prompt += \
            f"按这个JSON格式输出{output_format}，只能返回JSON，且JSON不要用```包裹，内容要用中文。"
