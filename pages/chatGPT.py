import streamlit as st
import title
import openai

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
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="여기에서 OpenAI API key를 발급받을 수 있습니다. https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
                # os.environ.get("OPENAI_API_KEY", None)  # local
             
        )

        st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown("---")
        # st.markdown("# About")
        # st.markdown(
        #     "📖KnowledgeGPT allows you to ask questions about your "
        #     "documents and get accurate answers with instant citations. "
        # )
        # st.markdown(
        #     "This tool is a work in progress. "
        #     "You can contribute to the project on [GitHub](https://github.com/mmz-001/knowledge_gpt) "  # noqa: E501
        #     "with your feedback and suggestions💡"
        # )
        # st.markdown("Made by [mmz_001](https://twitter.com/mm_sasmitha)")
        # st.markdown("---")


openai_api_key = st.session_state.get("OPENAI_API_KEY")

@st.cache_data(show_spinner=False)
def is_open_ai_key_valid(openai_api_key) -> bool:
    if not openai_api_key:
        st.error("좌측에 OpenAI API key를 입력하시오!")
        return False
    try:
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            api_key=openai_api_key,
        )
    except Exception as e:
        st.error(f"올바른 OpenAI API key가 아닙니다.")
        logger.error(f"올바른 OpenAI API key가 아닙니다.")
        #     st.error(f"{e.__class__.__name__}: {e}")
        # logger.error(f"{e.__class__.__name__}: {e}")
        return False
    return True

uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
)

if not uploaded_file:
    st.stop()
else :
    is_open_ai_key_valid(openai_api_key)


