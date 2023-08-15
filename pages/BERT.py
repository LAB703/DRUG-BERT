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

input = st.text_area('Input', """\
In some instances, it can be highly dangerous to use a medicine for the prevention or treatment of COVID-19 that has not been approved by or has not received emergency use authorization from the FDA.
""")

inputs = tokenizer.encode_plus(input, return_tensors="pt")
outputs = model(**inputs)
sequence_class_index = torch.argmax(outputs.sequence_logits, dim=-1)
sequence_class = model.sequence_tags[sequence_class_index[0]]
token_class_index = torch.argmax(outputs.token_logits, dim=-1)
tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[0][1:-1])
tags = [model.token_tags[i] for i in token_class_index[0].tolist()[1:-1]]

st.table(list(zip(tokens, tags)))
