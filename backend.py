from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from openai import OpenAI
import openai
from fastapi import FastAPI
from pydantic import BaseModel
import os
from inference_finetune import *
from Check_list_Few_shot import *
from Bad2good_request import *
from why_bad_request import *

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.post("/summarize")
def post_summarize(input_text: InputText):
    summary = finetuned_summarize(input_text.text)
    return {"summary": summary}

@app.post("/check_list")
def post_check_list(input_text: InputText):
    check_list = fewshot_checklist(input_text.text)
    return {"check-list": check_list}

@app.post("/bad2good")
def post_bad2good(input_text: InputText):
    bad2good = bad2good(input_text.text)
    return {"bad2good": bad2good}

@app.post("/why_bad_request")
def post_bad_request(input_text: InputText):
    bad_request = RAG_bad_request(input_text.text)
    return {"bad-request": bad_request}