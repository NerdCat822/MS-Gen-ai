from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def flag(text):
    system_instruction = "이 문장이 나쁘다면 False, 착하다면 True 를 출력해줘"

    messages = [{"role": "system", "content": system_instruction},
                {"role": "user", "content": text} 
                ]

    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    result = response.choices[0].message.content
    
    return result
