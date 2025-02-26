mport os

import streamlit as st  # Streamlit을 사용하여 웹 애플리케이션을 구축
from dotenv import load_dotenv  # 환경 변수 로드를 위한 라이브러리
from langchain import hub  # LangChain의 프롬프트 저장소
from langchain.agents import AgentExecutor, create_openai_tools_agent, load_tools  # 에이전트 관련 기능
from langchain.memory import ConversationBufferMemory  # 대화 메모리 관리
from langchain_community.callbacks import StreamlitCallbackHandler  # Streamlit에서 실행 상태를 표시하는 콜백 핸들러
from langchain_community.chat_message_histories import StreamlitChatMessageHistory  # 채팅 메시지 기록을 저장하는 클래스
from langchain_openai import ChatOpenAI  # OpenAI 모델을 LangChain에서 사용하기 위한 클래스

# 환경 변수 로드 (API 키 및 설정값 사용)
load_dotenv()

def create_agent_chain(history):
    """LangChain 에이전트를 생성하는 함수"""
    chat = ChatOpenAI(
        model_name=os.environ["OPENAI_API_MODEL"],  # 환경 변수에서 모델명 로드
        temperature=os.environ["OPENAI_API_TEMPERATURE"],  # 환경 변수에서 온도 설정 로드
    )
    
    tools = load_tools(["ddg-search", "wikipedia"])  # 사용할 도구(웹 검색 및 위키피디아 검색) 로드
    
    prompt = hub.pull("hwchase17/openai-tools-agent")  # LangChain 허브에서 프롬프트 가져오기
    
    memory = ConversationBufferMemory(
        chat_memory=history,  # 이전 채팅 기록을 저장할 메모리 설정
        memory_key="chat_history",  # 메모리 키
        return_messages=True  # 메시지를 반환하도록 설정
    )
    
    agent = create_openai_tools_agent(chat, tools, prompt)  # OpenAI 기반 에이전트 생성
    return AgentExecutor(agent=agent, tools=tools, memory=memory)  # 에이전트 실행 객체 반환

# Streamlit 애플리케이션 제목 설정
st.title("langchain-streamlit-app")

# 채팅 기록을 저장할 객체 생성
history = StreamlitChatMessageHistory()

# 이전 채팅 메시지를 화면에 출력
for message in history.messages:
    st.chat_message(message.type).write(message.content)
    
# 사용자 입력 받기
prompt = st.chat_input("What is up?")

if prompt:  # 사용자가 입력을 제공한 경우 실행
    with st.chat_message("user"):  # 사용자 입력 메시지를 화면에 표시
        st.markdown(prompt)
        
    with st.chat_message("assistant"):  # AI 응답을 화면에 표시
        callback = StreamlitCallbackHandler(st.container())  # 상태 표시를 위한 콜백 핸들러 생성
        agent_chain = create_agent_chain(history)  # LangChain 에이전트 생성
        response = agent_chain.invoke(
            {"input": prompt},  # 사용자 입력을 에이전트에 전달
            {"callbacks": [callback]},  # 상태 표시를 위한 콜백 추가
        )
        
        st.markdown(response["output"])  # 에이전트의 응답을 화면에 출력
