import os
import logging

from openai import OpenAI


class ChatGPTRewriter:
    def __init__(self):
        self.openai = OpenAI()

    def rewrite_title(self, title: str) -> str:
        logging.info(f"Original title: {title}")

        return self._request(
            f"rewrite text as title of article"
            f"translate it from Serbian to Russian"
            f"in one sentence and send only new version in Russian"
            f"without mention that it is a new version please\n\n{title}"
        )

    def rewrite_summary(self, summary: str) -> str:
        logging.info(f"Original summary: {summary}")

        return self._request(
            f"rewrite text as summary and keep only main idea"
            f"translate it from Serbian to Russian"
            f"send only Russian new version"
            f"without mention that it is a new version please\n\n{summary}"
        )

    def _request(self, request_message: str) -> str:
        # token = os.environ.get("OPENAI_API_KEY")
        # self.openai.api_key = token

        completion = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'user','content': request_message}
            ]
        )
        return completion.choices[0].message.content