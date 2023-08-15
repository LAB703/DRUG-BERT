import streamlit as st
import json
import torch
from transformers import BertTokenizerFast, BertForSequenceClassification

@st.cache(allow_output_mutation=True)
def load_model():
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-cased')
    model = BertForSequenceClassification.from_pretrained(
            "QCRI/PropagandaTechniquesAnalysis-en-BERT",
             revision="v0.1.0")
    return tokenizer, model
    
tokenizer, model = load_model()
