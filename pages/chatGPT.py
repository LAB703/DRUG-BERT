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


example_lst = ['a', 'b', 'c' ,'d', 'e']

def reset():
    st.session_state.selection = 'Please Select'

random_change = st.button('Reset 🔁', on_click=reset)

if random_change :
    example = random.choice(example_lst)
    st.write(example)
    examples = st.text_input(value = example, on_change = rest)
else : 
    st.stop()


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


