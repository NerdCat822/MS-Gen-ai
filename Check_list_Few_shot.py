from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.schema import BaseOutputParser
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.environ.get('OPENAI_API_KEY')

def fewshot_checklist(text):
    chat = ChatOpenAI(openai_api_key=openai_api_key, 
                      model = "gpt-3.5-turbo",
                      temperature=0.1)

    examples = [
        {
            "question": """
    왜 이런 일이 일어나고 있는 거야? 기초수급비용을 왜 이렇게 적게 주는 거야? 내가 이미 너희들에게 얼마나 돈을 받아야 하는데? 더 이상 날 괴롭히지 마! 내 돈으로 무엇을 하는지 말해봐!

    그냥 가라. 너희들은 어디서 이 모든 돈을 사용하고 있는 거야? 내가 도대체 뭘 위해서 받는 건데? 나는 이런 불공평한 일을 더 이상 참지 않겠어!

    민원인은 자신의 분노를 행정복지센터에 던지고, 기초수급비용에 대한 의문을 제기한 것으로 만족한다.
    """,
            "answer": """
    민원인께서 제기하신 우려와 질문들에 대해 소명하고 도움을 드리기 위해 다음과 같은 조치를 취하겠습니다.

    1번 업무: 기초수급비용에 대한 계산과 배정 설명
    - 민원인의 기초수급비용이 산정되는 기준과 계산 방식을 설명해 드리겠습니다. 그리고 민원인의 개인적인 사례가 어떻게 적용되었는지 구체적으로 검토하여, 현재 받고 계신 금액이 적절한지 다시 한 번 확인하겠습니다.

    2번 업무: 기초수급비용 관련 불만사항 접수 및 해결 방안 모색
    - 민원인의 불만사항을 정식으로 접수하고, 혹시 있을 수 있는 오류나 절차의 잘못을 조사하겠습니다. 또한, 민원인의 상황을 개선할 수 있는 다른 지원 프로그램이나 서비스에 대해서도 정보를 제공하겠습니다.

    3번 업무: 상담 및 이의 제기 절차 안내
    - 민원인이 기초수급비용과 관련하여 이의를 제기하고 싶을 경우, 해당 절차에 대해 안내하고 필요한 서류나 방법에 대해 상세히 설명해 드릴 것입니다. 이 과정에서 민원인의 권익을 보호하기 위한 절차를 안내해 드리겠습니다.

    4번 업무: 추가 지원 및 상담 서비스 안내
    - 현재 상황에서 민원인이 추가적인 지원을 받을 수 있는 방법에 대해서도 안내해 드리겠습니다. 사회복지사나 관련 전문가와의 상담을 통해서 민원인의 상황을 보다 깊이 있게 파악하고, 다양한 지원 방법을 모색하겠습니다.

    이러한 조치들을 통해 민원인께서 기초수급비용과 관련된 문제를 명확하게 이해하시고, 해당 문제를 해결할 수 있도록 최선을 다하겠습니다.
    """
        },
        {
            "question": """
    왜 아무 조치도 취하지 않는 거야? 4주 전부터 강남역 근처에 포트홀이 발생했는데, 왜 아무 것도 하지 않고 있는 거야? 이건 대체 뭐하는 거야?

    당장 이 문제를 해결해야 해! 강남역 주변은 교통이 매우 혼잡한 곳이고, 이 포트홀 때문에 교통 체증이 더 심해지고 있는 거야. 이건 단순히 불편한 문제가 아니라 안전 문제야! 왜 아무런 조치도 취하지 않는 거야?

    조사를 하느라고 시간을 끌어 대는 게 아니라, 이 문제를 해결해야지! 이런 무능력한 행정에 화가 나! 언제까지 이따위로 국민을 방치할 건데?
    """,
            "answer": """
    1번 업무: 포트홀 관련 민원 접수
    - 먼저, 강남역 근처 포트홀 발생 상황에 대해 말씀해 주셔서 감사합니다. 불편을 겪으신 점에 대하여 사과의 말씀을 드립니다. 민원을 등록하겠습니다.

    2번 업무: 조치 계획 안내
    - 조사 및 처리 과정에 대한 명확한 정보 제공과 함께, 조치 계획을 즉시 수립하여 안내드리겠습니다.
    - 현재 해당 포트홀에 대한 조사 진행 상황을 확인할 것이며, 만약 조사가 이미 완료되었다면, 조속한 시일 내에 보수 작업이 이루어지도록 관련 부서에 긴급하게 지시하겠습니다.

    3번 업무: 안전 조치
    - 이 포트홀로 인해 발생할 수 있는 안전 문제를 최소화하기 위하여 즉각적인 안전조치를 취하겠습니다. 예를 들어, 경고 표지판 설치나 임시 통제조치를 진행할 수 있습니다.

    4번 업무: 향후 대응 절차 안내
    - 이와 같은 문제가 재발하지 않도록 현재의 대응 절차를 검토하고, 가능한 개선 방안을 마련할 것입니다.

    5번 업무: 민원 처리 결과 통보
    - 민원 처리 과정과 결과에 대해 투명하게 공유하고, 완료되는 대로 말씀드리겠습니다. 개인 연락처나 이메일로 직접 연락 드릴 수 있도록 조치 사항을 알려주시면 감사하겠습니다.
    """
        },
        {
            "question": """
    왜 내가 불법주차를 했다는 거야? 나는 그런 걸 기억하지 않아! 이런 미친 짓을 왜 하는 거야? 겨우 3분 가지고 그러는거야? 내가 당장 그 돈을 내지 않으면 어떻게 되는 거야?

    너희들은 도대체 어떤 권한으로 나한테 벌금을 부과하는 거야? 이런 불법적인 과태료를 물리는 게 얼마나 무섭게나 불공평한 일인지 알고 있어?

    어떤 절차? 이런 불법주차에 대한 증거는 무엇이야? 나한테 어떤 증거도 없는데 이런 과태료를 부과하는 건 무슨 의미가 있어?
    """,
            "answer": """
    민원인님, 불법주차와 관련하여 불편을 겪으신 점에 대해 안타까움을 느끼며, 이 사항에 대해 조속히 해결책을 제시드리고자 합니다. 질문에 대한 답변은 아래와 같습니다.

    1번 업무: 불법주차 과태료에 대한 설명
    - 공공장소의 주차 규정을 위반한 차량에 대하여 지방자치단체 또는 관할 교통 단속 기관은 교통 법규에 따라 과태료를 부과할 수 있는 권한이 있습니다. 비록 3분이라는 짧은 시간이었을지라도 규정을 준수해야 하며, 이는 도로의 원활한 통행과 불법 주차로 인한 다른 시민들의 불편을 방지하기 위함입니다.

    2번 업무: 과태료 부과 절차 및 증거 안내
    - 과태료 부과에 관한 절차는 법령에 명시된 바와 같이 이행됩니다. 이에 따라 해당 불법주차의 증거로는 현장에 설치된 CCTV 영상, 사진 촬영, 단속 요원의 목격 등이 있을 수 있습니다. 
    - 민원인님께서 정확한 증거를 원하시는 경우, 불법주차 증거 자료에 대한 열람을 요청하실 수 있습니다. 해당 자료는 민원인님이 과태료 처분에 대해 이의를 제기하거나 정확한 상황을 파악하시는 데 도움이 될 것입니다.

    3번 업무: 과태료 미납 시의 조치 안내
    - 과태료를 납부 기한 내에 납부하지 않을 경우, 추가적인 가산금이 부과될 수 있으며, 장기 미납 시 재산에 대한 압류 등의 법적 조치가 이루어질 수 있습니다. 이를 피하기 위해서는 기한 내에 과태료를 납부하셔야 합니다.

    4번 업무: 이의 제기 방법 안내
    - 과태료에 대한 이의가 있으시다면, 과태료 처분 통지서상의 이의신청 기간 내에 해당 기관에 서면으로 이의 신청을 하여 사안에 관한 재검토를 요청할 수 있는 절차가 있습니다. 이의 신청 절차에 따라, 관할 기관에서는 신청을 접수하고 사실 관계를 확인한 후 그 결과를 민원인님께 통지합니다.

    민원인님의 문제 해결을 위해 최선을 다하겠습니다. 먼저, 불법주차에 대한 증거를 확인하고 싶으신 경우, 관할 기관에 연락하여 증거 자료 열람을 요청하실 수 있도록 안내해 드리겠습니다. 추가로 이의 신청 방법에 대해서도 자세히 설명해 드리겠습니다. 더 궁금하신 사항이 있으시면 언제든지 문의 바랍니다.
    """
        }
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{question}"),
            ("ai", "{answer}"),
        ]
    )

    example_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )


    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "assistant는 현재 공무원이다. 민원인의 입력을 분석하여 민원인이 원하는 바를 찾아내고, 1번 업무:, 2번 업무: 와 같은 형식으로 민원인이 원하는 바에 대한 나의 적절한 조치를 출력해줘."),
            example_prompt,
            ("human", "{input}"),
        ]
    )

    chain = final_prompt | chat

    return chain.invoke({"input": text})
