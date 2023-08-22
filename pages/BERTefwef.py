import streamlit as st
import json
import torch
from transformers import BertTokenizerFast, BertForSequenceClassification

import style
st.markdown(style.style, unsafe_allow_html=True)
    
@st.cache(allow_output_mutation=True)
    
def load_model(model_name_or_path):
    tokenizer = BertTokenizerFast.from_pretrained(model_name_or_path)
    model = BertForSequenceClassification.from_pretrained(model_name_or_path)
    return tokenizer, model
    
# tokenizer, model = load_model("bert-base-multilingual-cased")
tokenizer, model = load_model("beomi/kcbert-base")
text="누구든지 아동·청소년이용음란물임을 알면서 이를 소지하여서는 아니된다."
st.write(text)
tokenized_text = tokenizer.tokenize(text)
st.write('tokenized_text >>', tokenized_text)



import streamlit as st
import regex as re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
#import string
import plotly.express as px
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

def prep_text(text):
    """
    function for preprocessing text
    """

    # remove trailing characters (\s\n) and convert to lowercase
    clean_sents = [] # append clean con sentences
    sent_tokens = sent_tokenize(str(text))
    for sent_token in sent_tokens:
        word_tokens = [str(word_token).strip().lower() for word_token in sent_token.split()]
        #word_tokens = [word_token for word_token in word_tokens if word_token not in punctuations]
        clean_sents.append(' '.join((word_tokens)))
    joined = ' '.join(clean_sents).strip(' ')
    joined = re.sub(r'`', "", joined)
    joined = re.sub(r'"', "", joined)
    return joined


# model name or path to model
checkpoint = "sadickam/sdg-classification-bert"


# Load and cache model
@st.cache(allow_output_mutation=True)
def load_model():
    return AutoModelForSequenceClassification.from_pretrained(checkpoint)


# Load and cache tokenizer
@st.cache(allow_output_mutation=True)
def load_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    return tokenizer


st.markdown("##### Text Input")
with st.form(key="my_form"):
    Text_entry = st.text_area(
        "Paste or type text in the box below (i.e., input)"
    )
    submitted = st.form_submit_button(label="👉 Get SDG prediction!")

if submitted:

    # SDG labels list

    label_list = [
        '🚨⛔️🚫🔴: 마약광고',
        '✅🟡🟢: 마약광고 의심글',
        '🔵: 마약글 비해당'
    ]

    if Text_entry == "":
        st.warning(
            """This app needs text input to generate predictions. Kindly type or paste text into 
            the above **"Text Input"** box""",
            icon="⚠️"
        )

    elif Text_entry != "":

        # Pre-process text
        joined_clean_sents = prep_text(Text_entry)

        # tokenize pre-processed text
        tokenizer_ = load_tokenizer()
        tokenized_text = tokenizer_(joined_clean_sents, return_tensors="pt", truncation=True, max_length=512)

        # predict pre-processed
        model = load_model()
        text_logits = model(**tokenized_text).logits
        predictions = torch.softmax(text_logits, dim=1).tolist()[0]
        predictions = [round(a, 3) for a in predictions]

        # dictionary with label as key and percentage as value
        pred_dict = (dict(zip(label_list, predictions)))

        # sort 'pred_dict' by value and index the highest at [0]
        sorted_preds = sorted(pred_dict.items(), key=lambda x: x[1], reverse=True)

        # Make dataframe for plotly bar chart
        u, v = zip(*sorted_preds)
        x = list(u)
        y = list(v)
        df2 = pd.DataFrame()
        df2['SDG'] = x
        df2['Likelihood'] = y

        c1, c2, c3 = st.columns([1.5, 0.5, 1])

        with c1:
            st.markdown("##### Prediction outcome")
            # plot graph of predictions
            fig = px.bar(df2, x="Likelihood", y="SDG", orientation="h")

            fig.update_layout(
                # barmode='stack',
                template='seaborn',
                font=dict(
                    family="Arial",
                    size=14,
                    color="black"
                ),
                autosize=False,
                width=800,
                height=500,
                xaxis_title="Likelihood of SDG",
                yaxis_title="Sustainable development goals (SDG)",
                # legend_title="Topics"
            )

            fig.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=14))
            fig.update_yaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=14))
            fig.update_annotations(font_size=14)  # this changes y_axis, x_axis and subplot title font sizes

            # Plot
            st.plotly_chart(fig, use_container_width=False)
            st.success("SDG successfully predicted. ", icon="✅")

        with c3:
            st.header("")
            predicted = st.markdown("###### Predicted " + str(sorted_preds[0][0]))
            Prediction_confidence = st.metric("Prediction confidence", (str(round(sorted_preds[0][1] * 100, 1)) + "%"))
