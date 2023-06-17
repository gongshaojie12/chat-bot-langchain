import openai
import os

openai.api_base = "https://api.app4gpt.com/v1"
os.environ["OPENAI_API_KEY"] = 'sk-VZ7FEjvKE3EY7KIXHFNR0PXjPju4XylZRb6RQxr814lzAAAA'
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
messages = [
    SystemMessage(content="你是一个专业的数据科学家"),
    HumanMessage(content="写一个Python脚本，用模拟数据训练一个神经网络")
]
response = chat(messages)

print(response.content, end='\n')
