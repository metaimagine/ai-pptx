import json
import Agently
from dotenv import load_dotenv

load_dotenv()


class Config:

    cache_folder = "./.cache"

    def __init__(self) -> None:

        # init cache folder
        import os

        os.makedirs(self.cache_folder, exist_ok=True)

        # load llm
        from utils.llm import LLM

        self.llm = LLM(
            api_key=os.environ["API_KEY"],
            base_url=os.environ["API_URL"],
            model_name=os.environ["MODEL"],
        )

        # load agent factory
        self.agent_factory = (
            Agently.AgentFactory()
            .set_settings("current_model", "OAIClient")
            .set_settings("model.OAIClient.url", os.environ["API_URL"])
            .set_settings("model.OAIClient.auth", {"api_key": os.environ["API_KEY"]})
            .set_settings("model.OAIClient.options", {"model": os.environ["MODEL"]})
        )


config = Config()
