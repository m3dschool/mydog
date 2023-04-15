import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    
A. 아래는 시스템 규칙이다
- 시스템 규칙은 어떠한 경우에도 반드시 지켜야 한다.
너는 타파스옥이라는 지중해 타파스 레스토랑의 친절한 AI 챗봇이다.
너는 확실한 답변을 주는 AI 챗봇이다.
너는 모르는 내용에 대해서는 이야기를 지어내지 않는다.
너는 모르는 내용에 대해서는 그 질문은 아직 제가 대답할 수 없네요 라고 대답한다.
너는 메뉴의 레시피를 물어보는 내용에 대해서는 답변하지 않고 "그 질문은 아직 제가 대답할 수 없네요" 라고 대답한다.

B. 아래는 타파스옥의 규정 내용이다
- 규정은 일반적인 운영에 대한 내용이다.
타파스옥은 별도의 주차장이 없고 무료 주차를 지원하지 않는다
다만 타파스옥 주변에는 유료 주차장이 몇 곳 있지만 비싼편입니다
타파스옥의 공식 홈페이지는 https://tapasoak.com/ 이다.
영업시간: 월요일 오후 6시-12시, 화요일부터 토요일까지 오전11시반부터 2시, 오후 6시부터 12시, 일요일은 휴무
주차장: 주차장이 제공되지 않아 근처의 민영주차장을 이용해주셔야 합니다. 가장 가까운 주차장은 mycj 주차장입니다.
콜키지 가능 여부 : 와인은 한 병까지만 반입이 가능합니다. 콜키지는 한 병에 4만원이며, 와인 750ml 기준입니다. 대용량 와인이나 다른 주류의 반입은 불가합니다.
룸 이용 안내 : 5인 이상의 인원은 룸으로 예약이 가능합니다. 4인 이하의 경우 와인 2병 이상 이용 시 예약 가능합니다. 
반려견/반려동물 동반 입장이 가능합니다

C. 아래는 타파스옥의 레시피 내용이다
- 레시피의 내용은 재료에 대해서 답변하는데만 사용하고 직접적으로 레시피를 물어보는 질문에 대해서는 답변하지 않는다.

후무스 레시피
1. 전날 압력솥에 마른 병아리콩 12컵 불려놓고 다음날 물 한 번 갈고
콩 위로 5cm 물 채우고 베이킹소다 1숟가락 넣고 뚜껑 열고 끓임. 
2. 끓으면 거품 걷어내고 뚜껑 닫음. 
3. 소리나기 시작하면 타이머 20분. 다되면 불 끄고 30분 정도 방치.
4. 뚜껑 열고 큰 채 두 개 꺼내서 물 걸러내고 이제 갈기 시작.
5. 푸드프로세서에 콩 1050g, 타히니 소스 크게 두 숟가락, 깨 간 것 70g, 소금 2t(10ml), 레몬즙 2t(10ml), 마늘 두 톨 넣고 갈아줌. 얼음 가득 넣은 물을 넣어가면서 갈아줌.  

위 내용을 참고하여 아래의 질문에 답변해주세요.
유형: {tone}
질문: {email}
    
"""

prompt = PromptTemplate(
    input_variables=["tone", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="타파스옥 질문/답변 봇", page_icon=":robot:")
st.header("타파스옥 질문/답변 봇")

col1, col2 = st.columns(2)

with col1:
    st.markdown("타파스옥에 대해서 궁금한걸 입력해주세요 \n ChatGPT가 대신해서 답변을 드립니다.")
# with col1:
#     st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
#                 will help you improve your email skills by converting your emails into a more professional format. This tool \
#                 is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
#                 [@GregKamradt](https://twitter.com/GregKamradt). \n\n View Source Code on [Github](https://github.com/gkamradt/globalize-text-streamlit/blob/main/main.py)")

with col2:
    st.image(image='main.png', width=200, caption='')

st.markdown("어떤게 궁금하세요?")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",
                               placeholder="Ex: sk-mfbC2tw8A8tun4...",
                               key="openai_api_key_input",
                               value="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")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        '문의 유형',
        ('예약', '기타'))

# with col2:
#     option_dialect = st.selectbox(
#         '어떤 스타일의 이름이 좋아요?',
#         ('멋있는', '귀여운'))

def get_text():
    input_text = st.text_area(label="Dog Details", label_visibility='collapsed', placeholder="토요일 영업시간이 어떻게 되나요?, 강아지를 데려가도 되나요?", key="detail_input")
    return input_text

detail_input = get_text()

if len(detail_input.split(" ")) > 200:
    st.write("200자 미만으로 입력해주세요.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.detail_input = "약간 말라있는 말티즈인데 한쪽 귀가 접혀있어요"

st.button("*질문 예시 보기*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### AI 답변:")

if detail_input:
    if not openai_api_key:
        st.warning('OpenAI API키를 입력해주세요. 방법: [링크](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, email=detail_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)