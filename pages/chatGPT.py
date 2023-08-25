import streamlit as st
import title
import openai

title.header()
# https://ask-my-pdf.streamlit.app/
#https://gpt4autocoder.streamlit.app/
# https://knowledgegpt.streamlit.app/
# https://langchain-chat-search.streamlit.app/
# https://langchain-quickstart.streamlit.app


openai_api_key = st.session_state.get("OPENAI_API_KEY")


if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )


uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
)

if not uploaded_file:
    st.stop()
