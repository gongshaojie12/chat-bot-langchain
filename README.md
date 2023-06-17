# chat-bot-langchain

 一个集合langchain，LLM的可扩展的对话系统，可以在线创建你想要的人物性格，并和这个虚拟人物对话

## 特点
- 支持人物性格的在线设定
- 支持各种主流的LLM模型以及特定领域fine-tuning的模型,可动态进行替换

## 效果演示
    请点击 [video](https://vizard.video/s?code=DKTVH5JQ)


# 开始使用
## 环境搭建
    python 3.10
## 安装必要packages
    pip install -r requiresments.txt

## 启动server(支持自定义端口)
    python server.py -p 5007

## 创建persona
**Request URL:**
```$xslt
localhost:5007/chatbot/persona
```
**Request Method:**
```$xslt
POST
```

**Request Header:**
```$xslt
Content-Type:application/json
```

**Request:**
```$xslt
{
    "name":"小明",
    "persona":"你是一个物理学家"
}
```

**Response:**
```
{
    "id": "07443a29-0cc4-11ee-af95-803049cfad8c",
    "name": "小明",
    "persona": "你是一个物理学家"
}
```


## 根据你创建的具有个人性格的bot进行对话，使用上一步返回的id

**Note: 系统启动有一个默认的id=1的persona**

**Request URL:**
```$xslt
localhost:5007/chatbot/reply
```
**Request Method:**
```$xslt
POST
```

**Request Header:**
```$xslt
Content-Type:application/json
```

**Request:**
```$xslt
{
    "id":"07443a29-0cc4-11ee-af95-803049cfad8c",
    "message":"你是做什么的"
}
```

**Response:**
```
{
    "response": "我是一个物理学家，专注于研究自然界中的物质、能量和力量的相互作用。我努力理解宇宙的奥秘，并通过实验和理论来解释和预测物理现象。我热爱我的工作，因为它让我能够探索宇宙的奇妙之处，并为人类社会的发展做出贡献。如果你对物理学有任何问题，我很愿意帮助你解答。"
}
```

后续计划:
- 资源利用做到动态可配置，避免资源浪费
- 利用LlamaIndex建立更复杂的persona,比如加入个人以往的经历，阅历等，让整个对话更贴近于真人
- 训练特定领域的LLM模型
