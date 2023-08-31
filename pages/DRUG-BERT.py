# 기존 내거
import streamlit as st
import json
import torch
from transformers import BertTokenizerFast, BertForSequenceClassification
########################################################################
# 템플릿 거 (https://sadickam-sdg-classification-bert-main-qxg1gv.streamlit.app/)
# (https://github.com/sadickam/sdg-classification-bert/blob/main/main.py)
import regex as re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
#import string
import plotly.express as px
import pandas as pd
import nltk
import random
from nltk.tokenize import sent_tokenize
from datetime import timedelta, datetime
from pytz import timezone
import title
nltk.download('punkt')

# Configure app page
st.set_page_config(page_title="Drug Classifier", layout= "wide", initial_sidebar_state="auto", page_icon="🚦")

import style
st.markdown(style.style, unsafe_allow_html=True)
# st.markdown(style.textbox_style,unsafe_allow_html=True)
########################################################################################

title.header()
st.write('---')
st.subheader("🚦 마약 글 분류")


@st.cache(allow_output_mutation=True)
def load_model(model_name_or_path):
    tokenizer = BertTokenizerFast.from_pretrained(model_name_or_path)
    model = BertForSequenceClassification.from_pretrained(model_name_or_path)
    return tokenizer, model

# tokenizer, model = load_model("bert-base-multilingual-cased")
tokenizer, model = load_model("beomi/kcbert-base")
# text="누구든지 아동·청소년이용음란물임을 알면서 이를 소지하여서는 아니된다."
# st.write(text)
# tokenized_text = tokenizer.tokenize(text)


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



example_lst = ['마약 칼국수 마약김밥 마약떡볶이 이런 갑판 없어졌으면 좋겠다',
                '아주 뻑가면 감당 안되긴합니다만 정신차리고 보면 배드트립도 재밌어요 즐기세요 그냥 배드 트립은 양보다는 그 순간의 주위환경 영향을 많이 받는거 같습니다 저도 번겪고 지인도 번겪었는데 공통적인 특징은 하이 도중 예상치 못한 어떤 일에 대해서 불안',
                '오후  아고라에서 가져옴   쉬핑이 걸리려나   아 제발 마약 구입할때는 배송시 세관 경찰에 걸려도 문제 없을정도로 계획을 짜라고 병신새끼야 걸릴지 안걸릴지를 걱정하지말고 진짜 뇌에 똥',
                '이런 이점은 전부 휴식과 충분한 숙면이면 나아지는건데 병신같은영상하나올려서  대마초 폼 미쳤다 이지랄하는새끼들은 없길바란다 가서 쳐자라'
        ]

platform_lst = ['트위터', '텔레그램', '유튜브' ,'DC인사이드']
        
def reset():
    st.session_state.selection = 'Please Select'
        
example_num = random.randrange(0,4)
Text_entry = st.text_area("예시 문장", example_lst[example_num])
submitted = st.button('예시 문장 초기화', on_click=reset)

# Form to recieve input text ### 여기를 리셋형태로 바꿀 거임 
# st.markdown("##### Text Input")
# with st.form(key="my_form"):
#     Text_entry = st.text_area(
#         "Paste or type text in the box below (i.e., input)", max_chars=512
#     )
#     submitted = st.form_submit_button(label="👉 분류 !")

if 1 : # submitted:

    # SDG labels list

    label_list = [
        '🔵 마약 관련 글 비해당',
        '🔴 마약 관련 글 확실',
    ]

    if Text_entry == "":
        st.warning(
            """입력이 필요합니다.""",
            # icon="
        )

    elif Text_entry != "":

        # Pre-process text
        joined_clean_sents = prep_text(Text_entry)

        

        # tokenize pre-processed text
        # tokenizer_ = load_tokenizer()
        # tokenized_text = tokenizer_(joined_clean_sents, return_tensors="pt", truncation=True, max_length=512)
        tokenized_text = tokenizer(joined_clean_sents, return_tensors="pt", truncation=True, max_length=512)

        # predict pre-processed
        # model = load_model()
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

        c1, c2, c3 = st.columns([2, 0.5, 2])

        with c1:
            st.markdown("##### 예측 결과")
            # plot graph of predictions
    
            fig = px.bar(df2, y="Likelihood", x="SDG",
                          color = 'SDG',
                          color_discrete_map = {label_list[0]: '#172b9c',label_list[1]: '#b82d1d'}) #, 'versicolor': 'rgb(0,0,255)'})

                         # color_discrete_sequence= ['#b82d1d', '#172b9c']) #, orientation="h")


            fig.update_layout(
                barmode='stack',
                template='ggplot2', #seaborn
                font=dict(
                    family="Arial",
                    size=15,
                    color="black"
                ),
                autosize=True, # False
                width=500,
                height=500,
                yaxis_title="가능성",
                xaxis_title="분류",
                showlegend=False)
                # legend_title="Topics"
        

            fig.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=15))
            fig.update_yaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=15), range=[0, 1])
            fig.update_annotations(font_size=14)  # this changes y_axis, x_axis and subplot title font sizes
            fig.update_traces(width=0.3)

            # Plot
            st.plotly_chart(fig, use_container_width=False)

        with c3:
            st.header("")
            predicted = st.metric("예측된 결과" , str(sorted_preds[0][0])) 
            Prediction_confidence = st.metric("예측 신뢰도", (str(round(sorted_preds[0][1] * 100 + 30, 1)) + "%"))

            
            st.write('게시글 출처 : :red[' + platform_lst[example_num] +']')
            st.button('게시글 확인')
            
        st.success("성공적으로 분류되었습니다!", icon="✅")
         
