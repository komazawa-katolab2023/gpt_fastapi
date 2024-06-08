from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
import os
import openai
from openai import OpenAI
import uvicorn

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY").strip()

client = OpenAI()

# 会話履歴を保持するリスト
conversation_history = []

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("../templates/index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.post("/ask")
async def ask(user_input: str = Form(...), gpt_model: str = Form(...)):
    system_prompt = "あなたはAIアシスタントです。"
    response = client.chat.completions.create(
    model=gpt_model,
    messages=[
        {"role": "system","content":system_prompt},
        {"role": "user", "content":user_input},
    ]
    )
    result = response.choices[0].message.content

    # 会話履歴に追加
    conversation_history.append({'user': user_input, 'bot': result})

    return JSONResponse(content={'response': result})

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)