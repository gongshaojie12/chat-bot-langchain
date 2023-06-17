from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
import os
import openai


class Personas:
    def __init__(self, persona):
        openai.api_base = "https://api.app4gpt.com/v1"
        os.environ["OPENAI_API_KEY"] = 'sk-VZ7FEjvKE3EY7KIXHFNR0PXjPju4XylZRb6RQxr814lzAAAA'
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
        self.system_message = SystemMessage(content="{}. {}".format(persona, "你的回复要有亲切感"))

    def predict(self, prompt):
        human_message = HumanMessage(content=prompt)
        messages = [
            self.system_message,
            human_message
        ]
        response = self.chat(messages)
        return response.content
