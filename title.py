import streamlit as st
from datetime import timedelta, datetime
from pytz import timezone

def header() :
  t1, t2, t3 = st.columns((2,5,3)) 
  # Korean_National_Police_Agency_Emblem
  t1.image('images/index.png', width = 120)
  t2.header('SNS 마약 거래 모니터링 시스템')
  tz = timezone('Asia/Seoul')
  re_run = t3.button('🔄 모델 갱신')
  if re_run :
      st.experimental_rerun()
      last_update = datetime.now(tz).strftime("%Y-%m-%d %A %H:%M")
  else : 
      last_update = datetime.now(tz).strftime("%Y-%m-%d %A %H:00")
  
  t3.write(datetime.now(tz).strftime("%Y-%m-%d %A %H:%M"))
  t3.write('마지막 갱신 : ' + last_update)
    
  st.write('')

