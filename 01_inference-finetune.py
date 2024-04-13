from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

model = "ft:gpt-3.5-turbo-1106:nerdcat822::9DZMWdZy"

llm = ChatOpenAI(model=model)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "'{input}' 이 내용 bullet point 사용해서 3줄 요약해줘"),
        ("user", "{input}" )
    ]
)

sentiment_chain = prompt_template | llm | StrOutputParser()

bad_texts_3 = """
왜 아무 조치도 취하지 않는 거야? 4주 전부터 강남역 근처에 포트홀이 발생했는데, 왜 아무 것도 하지 않고 있는 거야? 이건 대체 뭐하는 거야?

당장 이 문제를 해결해야 해! 강남역 주변은 교통이 매우 혼잡한 곳이고, 이 포트홀 때문에 교통 체증이 더 심해지고 있는 거야. 이건 단순히 불편한 문제가 아니라 안전 문제야! 왜 아무런 조치도 취하지 않는 거야?

조사를 하느라고 시간을 끌어 대는 게 아니라, 이 문제를 해결해야지! 이런 무능력한 행정에 화가 나! 언제까지 이따위로 국민을 방치할 건데?
"""

tt = "안녕하세요, 학생 여러분. 오늘 저는 반려동물의 복지와 건강을 위한 간호 목표와 실행에 대해 강의드리도록 하겠습니다. 반려동물을 키우는 사람이라면 반드시 알아야 할 내용입니다. 그럼 시작하겠습니다."

'''
response = client.chat.completions.create(
  model=model,
  messages=[
    {"role": "system", "content": "assistant는 user의 입력을 bullet point로 3줄 요약해준다."},
    {"role": "user", "content": tt}
  ]
)
print(response.choices[0].message.content)
'''
#sentiment_chain.invoke({"input":bad_texts_3})
print(sentiment_chain.invoke({"input":tt}))