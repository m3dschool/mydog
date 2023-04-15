import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    아래의 특성들을 이용해서 한글로 강아지 이름을 만들어주세요!
    이름만 단답형으로 최대 5개를 답변해 주세요.
    
    색상: {tone}
    스타일: {dialect}
    설명: {email}
    
    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="AI 강아지 이름 생성기", page_icon=":robot:")
st.header("AI 강아지 이름 생성기")

col1, col2 = st.columns(2)

with col1:
    st.markdown("오늘 새로운 강아지를 만나게 되었어요.\
                어떤 이름을 지어줄까요?")
# with col1:
#     st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
#                 will help you improve your email skills by converting your emails into a more professional format. This tool \
#                 is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
#                 [@GregKamradt](https://twitter.com/GregKamradt). \n\n View Source Code on [Github](https://github.com/gkamradt/globalize-text-streamlit/blob/main/main.py)")

with col2:
    st.image(image='main.png', width=500, caption='')

st.markdown("강아지에 대해서 알려주세요")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-mfbC2tw8A8tun4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        '강아지는 무슨색이에요?',
        ('흰둥이', '검둥이'))
    
with col2:
    option_dialect = st.selectbox(
        '어떤 스타일의 이름이 좋아요?',
        ('멋있는', '귀여운'))

def get_text():
    input_text = st.text_area(label="Dog Details", label_visibility='collapsed', placeholder="강아지에대한 설명을 간단히 적어주세요", key="detail_input")
    return input_text

detail_input = get_text()

if len(detail_input.split(" ")) > 200:
    st.write("200자 미만으로 입력해주세요.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.detail_input = "약간 말라있는 말티즈인데 한쪽 귀가 접혀있어요"

st.button("*이름 예시 보기*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### 당신의 강아지 이름:")

if detail_input:
    if not openai_api_key:
        st.warning('OpenAI API키를 입력해주세요. 방법: [링크](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=detail_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)