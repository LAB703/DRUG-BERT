import streamlit as st
import json
import torch
from transformers import BertTokenizerFast, BertForSequenceClassification

@st.cache(allow_output_mutation=True)
def load_model(model_name_or_path):
    tokenizer = BertTokenizerFast.from_pretrained(model_name_or_path)
    model = BertForSequenceClassification.from_pretrained(model_name_or_path)
    return tokenizer, model
    
tokenizer, model = load_model("bert-base-multilingual-cased")

text="누구든지 아동·청소년이용음란물임을 알면서 이를 소지하여서는 아니된다."
st.write(text)
tokenized_text = tokenizer.tokenize(text)
st.write('tokenized_text >>', tokenized_text)
