from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from operator import itemgetter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.document_loaders import PyPDFLoader, UnstructuredFileLoader, TextLoader
from langchain.chains import RetrievalQA
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.environ.get('OPENAI_API_KEY')

model = ChatOpenAI(openai_api_key=openai_api_key, 
                  model = "gpt-3.5-turbo",
                  temperature=0.1)

splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n",
    chunk_size = 600,
    chunk_overlap=100,
)

#loader = PyPDFLoader("./공공부문-특별악성고질민원-대응-매뉴얼.pdf") # pdf loader
loader =PyPDFLoader("./민원 처리에 관한 법령 해설집(개정판).pdf") # pdf loader

docs = loader.load_and_split(text_splitter=splitter)
#len(pages) 
#pages[2] 


# 문서 1페이지도 너무 김, CharacterTextSplitter로 \n 별로 나누기, 100음절 단위로 나누기, chunk_overlap=0이라서 겹치는 부분 X
#text_splitter = CharacterTextSplitter(separator="\n", chunk_size=600, chunk_overlap=0, length_function=len)
texts = splitter.split_documents(docs)

#len(texts) # 581 / 18 페이지 -> 581개의 chunk로 나눔 : 그림의 Transform 한 것
#texts[10] # Document(page_content='\uf3d0남녀의 성향이나 조건을...)

embeddings = OpenAIEmbeddings() # 문서 embeding 수행
db = FAISS.from_documents(texts, embeddings) # db 수행

# 검색, k:10 / 10개 (관련도 높은Top 10) 씩 찾기
#retriever = db.as_retriever(search_kwargs={"k": 20})
retriever = db.as_retriever()

# "주선자의 역할" 과 관련된 문서 검색
#rel_docs = retriever.get_relevant_documents("악성민원 대응")

#rel_docs[0]
#rel_docs[:3] # 관련도 높은 순으로 3개

#len(rel_docs) # 10 / 연관된 10개 문서
#print(rel_docs) # 문자열만 확인

chain = RetrievalQA.from_chain_type(
    llm=model,
    chain_type="refine", # 그 외에도 refine, map_reduce, map_rerank 존재
    retriever=db.as_retriever(),   
)
bad_text = """
왜 내가 불법주차를 했다는 거야? 씨발! 나는 그런 걸 기억하지 않아! 이런 미친 짓을 왜 하는 거야? 겨우 3분 가지고 그러는거야? 내가 당장 그 돈을 내지 않으면 어떻게 되는 거야?

너희들은 도대체 어떤 권한으로 나한테 벌금을 부과하는 거야? 이런 불법적인 과태료를 물리는 게 얼마나 무섭게나 불공평한 일인지 알고 있어?

어떤 절차? 이런 불법주차에 대한 증거는 무엇이야? 나한테 어떤 증거도 없는데 이런 과태료를 부과하는 건 무슨 의미가 있어?
"""

text = chain.invoke("악성민원과 관련해 민원처리법 몇조, 몇항과 관련해서 알려줘.")
print(text['result'])