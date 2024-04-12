
import json


class Config(object):

    cache_folder = "./cache"

    def __init__(self) -> None:

        # init cache folder
        import os
        os.makedirs(self.cache_folder, exist_ok=True)

        # load llm
        with open("setting.json", "r") as file:
            setting = json.load(file)
        from utils.llm import LLM
        self.llm = LLM(
            api_key=setting["llm"]["api_key"],
            base_url=setting["llm"]["base_url"],
            model_name=setting["llm"]["model_name"],
        )


config = Config()
