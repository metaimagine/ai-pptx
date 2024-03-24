from openai import OpenAI


class LLM:
    def __init__(self, api_key, base_url=None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, messages: list, model_name: str, temperature: float):
        """对话返回迭代器"""
        r = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        for chunk in r:
            c = chunk.choices[0].delta.content
            if not c:
                continue
            yield c

    def chat_in_all(self, messages: list, model_name: str, temperature: float):
        """对话返回全部内容"""
        r = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        collected = []
        for chunk in r:
            c = chunk.choices[0].delta.content
            if not c:
                continue
            collected.append(c)
        return ''.join(collected)

    def chat_once(self, prompt: str, model_name: str, temperature: float = 0.1, system_prompt: str = None):
        """一次性对话"""
        messages = [
            {"role": "system", "content": system_prompt or "你是个全能助手"},
            {"role": "user", "content": prompt}
        ]
        return self.chat_in_all(messages, model_name, temperature)
