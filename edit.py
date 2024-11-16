import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

st.title('봉사활동 신청서 작성 도우미')

# API 키 입력
api_key = st.text_input("Google API Key를 입력하세요", type="password")

if api_key:
    # 입력 필드
    name = st.text_input("이름")
    strengths = st.text_area("장점")
    weaknesses = st.text_area("단점")
    service_needs = st.text_area("필요한 봉사활동")

    # 모든 필드가 채워졌는지 확인
    all_fields_filled = bool(name and strengths and weaknesses and service_needs)

    # 프롬프트 템플릿 설정
    template = """
    다음 정보를 바탕으로 봉사활동 신청서를 작성해주세요:
    - 이름: {name}
    - 장점: {strengths}
    - 단점: {weaknesses}
    - 필요한 봉사활동: {service_needs}
    
    신청서는 자연스러운 문장으로 작성해주시고, 장점과 단점을 잘 설명하면서 왜 이 봉사활동이 필요한지 설득력 있게 작성해주세요.
    """

    prompt = PromptTemplate(
        input_variables=["name", "strengths", "weaknesses", "service_needs"],
        template=template
    )

    # 버튼이 모든 필드가 채워졌을 때만 활성화되도록 수정
    if st.button("신청서 생성", disabled=not all_fields_filled):
        try:
            # Gemini 모델 설정
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.0-pro",
                google_api_key=api_key,
                temperature=0.7
            )
            
            # 프롬프트 생성
            final_prompt = prompt.format(
                name=name,
                strengths=strengths,
                weaknesses=weaknesses,
                service_needs=service_needs
            )
            
            # 결과 생성
            response = llm.invoke(final_prompt)
            
            # 결과 표시
            st.subheader("생성된 신청서:")
            st.write(response.content)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
else:
    st.warning("API 키를 입력해주세요.")
