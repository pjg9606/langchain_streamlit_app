# LangChain Streamlit 앱

## 개요
이 프로젝트는 LangChain과 OpenAI API를 활용하여 Streamlit 기반의 챗봇을 구현한 애플리케이션입니다.

## 주요 기능
- OpenAI 기반 챗봇
- 대화 내역 저장 및 활용
- DuckDuckGo 및 Wikipedia 검색 기능
- Streamlit UI 제공

## 실행 방법
1. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```
2. 환경 변수 설정 (`.env` 파일 생성 후 API 키 추가)
3. Streamlit 실행:
   ```bash
   streamlit run app.py
   ```

## 파일 구조
```
langchain-streamlit-app/
│── app.py                # 메인 애플리케이션 코드
│── requirements.txt      # 필요한 패키지 목록
│── .env                  # 환경 변수 설정 파일
│── README.md             # 프로젝트 문서
```

## 기여
기능 개선 및 버그 수정 PR을 환영합니다!

