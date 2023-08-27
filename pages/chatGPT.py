import streamlit as st
import title
import openai
import random

title.header()
# https://ask-my-pdf.streamlit.app/
#https://gpt4autocoder.streamlit.app/
# https://knowledgegpt.streamlit.app/
# https://langchain-chat-search.streamlit.app/
# https://langchain-quickstart.streamlit.app

with st.sidebar:
        st.markdown(
            "## 사용법\n"
            "1. 🔑 [OpenAI API key](https://platform.openai.com/account/api-keys)를 입력하세요. \n"  # noqa: E501
            "2. 📄 구글에서 크롤링된 파일을 입력하세요. \n"
            "3. 💬 실행을 누르세요.\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="OpenAI API key를 입력하세요. (sk-...)",
            help="여기에서 OpenAI API key를 발급받을 수 있습니다. https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
                # os.environ.get("OPENAI_API_KEY", None)  # local       
        )

        st.session_state["OPENAI_API_KEY"] = api_key_input
        st.markdown("---")
        

openai_api_key = st.session_state.get("OPENAI_API_KEY")


example_lst = ['예시 문장 1', '예시 문장 2', '예시 문장 3' ,'예시 문장 4', '예시 문장 5']

with st.expander("사용된 프롬프트") :
        st.code('''for e in extracts :
          prompt = f"""
          prompt : 아래의 [extract]에서 텔레그램 아이디를 추출해야합니다. 예시는 [example]와 같습니다. 
        
          [example]
              input: 101서울떨액상구매(텔레@WICEW양산케타민팝니다ꗾ광주 ...
              output : WICEW
        
              input: 텔tktls44 #떨팝니다 #대마팝니다 #대마구하는방법 #허브
              output : tktls44
        
              input:떨팝니다텔레tyson779몰리판매작대기팝니다카톡tyson898 ...
              output : tyson779
        
              input: 떨 구입 (ㅌㄹ@zedice) 떨판매 떨구매 떨파는곳 떨팝니다 제더아이스 안녕하세요.각종 물건 판매하는 제더입니다. 안전을 최우선으로 2년동한 거래 ...
              output :  zedice
        
              input : 엑스터시구매-카톡:aky33 텔레:kid333 — '엑스터시,엑스터시판매,엑스터시파는곳,엑스터시사는
              output : kid333
        
        
          [extract]
          {e}
        
          """
          response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
              {"role": "user",
              "content": prompt}
            ]
          )
          print(response["choices"][0].message.content)''')

def reset():
    st.session_state.selection = 'Please Select'

st.button('Reset', on_click=reset)
st.text_input("", random.choice(example_lst))


@st.cache_data(show_spinner=False)
def is_open_ai_key_valid(openai_api_key) -> bool:
    if not openai_api_key:
        st.warning("좌측에 OpenAI API key를 입력하시오!")
        return False
    try:
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            api_key=openai_api_key,
        )
    except Exception as e:
        st.error(f"올바른 OpenAI API key가 아닙니다. 키를 재확인하세요.")
        # logger.error(f"올바른 OpenAI API key가 아닙니다. ")
        #     st.error(f"{e.__class__.__name__}: {e}")
        # logger.error(f"{e.__class__.__name__}: {e}")
        return False
    return True

uploaded_file = st.file_uploader(
    "Upload a csv, txt, or json file",
    type=["csv", "txt", "json"],
    help="파일을 업로드 하세요.",
)

if not uploaded_file:
    st.stop()
else :
    is_open_ai_key_valid(openai_api_key)


