import streamlit as st
from datetime import timedelta, datetime
from pytz import timezone


def header() :
  t1, t2, t3 = st.columns((2,4,2)) 
  # Korean_National_Police_Agency_Emblem
  t1.image('images/index.png', width = 120)
  t2.header('SNS 마약 거래 모니터링 시스템')
  t3.write(datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %A %H:%M:%S"))
  st.write('')
  st.write('')
  st.write('')
  st.write('---')
