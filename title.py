import streamlit as st
from datetime import timedelta, datetime
from pytz import timezone

def formatting(time_now) :
    weekday_dict = {
    0: '(월)',
    1: '(화)',
    2: '(수)',
    3: '(목)',
    4: '(금)',
    5: '(토)',
    6: '(일)'
    }

    tz = timezone('Asia/Seoul')
    formatted_time = time_now.strftime("%Y년 %m월 %d일") + ' ' + str(time_now.weekday()) + time_now.strftime("%I:%M") # weekday_dict[time_now.weekday()] + ' ' time_now.strftime("%I:%M")
    
    return formatted_time

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
  t3.write(formatting(datetime.now(tz))
  t3.write('마지막 갱신 : ' + last_update)
    
  st.write('')
  st.write('')
  st.write('')
  st.write('---')

# def header() :
#   t1, t2, t3 = st.columns((2,5,3)) 
#   # Korean_National_Police_Agency_Emblem
#   t1.image('images/index.png', width = 120)
#   t2.header('SNS 마약 거래 모니터링 시스템')
#   re_run = t3.button('🔄 모델 갱신')
#   time_now = datetime.now()
#   # formatted_time = time_now.strftime("%Y년 %m월 %d일") + ' ' + weekday_dict[time_now.weekday()] + ' ' + ampm_dict[time_now.strftime("%p")] + ' ' + time_now.strftime("%I:%M")

#   if re_run :
#       st.experimental_rerun()
#       last_update = datetime.now() #tz)
#   else : 
#       last_update = datetime.now() #tz)
  
#   t3.write(datetime.now() # tz))
#   t3.write('마지막 갱신 : ' + last_update)
#   st.write('')
#   st.write('---')
