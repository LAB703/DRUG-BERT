# -*- coding: utf-8 -*-

import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta, datetime
from pytz import timezone

st.set_page_config(page_title='SNS 모니터링',  layout='wide', page_icon='🚔')

# import style
# st.markdown(style.style, unsafe_allow_html=True)


with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# st.sidebar.success("Select a demo above.")
#this is the header

t1, t2, t3 = st.columns((2,5,3)) 
# Korean_National_Police_Agency_Emblem
t1.image('images/index.png', width = 120)
t2.header('SNS 마약 거래 모니터링 시스템')
t3.write(datetime.now(timezone('Asia/Seoul')).strftime("%Y-%m-%d %A %H:%M:%S"))
re_run = t3.button('🔄 모델 갱신')
st.write('')
st.write('')
st.write('')
st.write('---')

if re_run :
    st.experimental_rerun()
    
# t2.markdown(" **tel:** 01392 451192 **| website:** https://www.swast.nhs.uk **| email:** mailto:data.science@swast.nhs.uk")


drug_slang_list = ["대마","대마초", "대마유", "디아제팜", "마리화나","메스암페타민", "몰리", "몰핀", "물봉", "물뽕", "아편", "아이스",  
                        "LSD" ,"양귀비", "엑스터시", "엘에스디", "작대기", "코카인", "해시시", "필로폰", "히로뽕", "헤로인", "모르핀"] 

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📈 전체", "🐦 트위터", "📨 텔레그램", "▶️ 유튜브", "🌌 DC인사이드",  "💀 다크웹",  "🏴‍☠️ 다크웹2"])

for drug in drug_slang_list :
    print('')
    

with tab2 : 
    # drug = pd.read_csv('data/트위터/csv/작대기.csv', index_col = 0)
    print('')

## Data

with st.spinner('Updating Report...'):
    
    #Metrics setting and rendering
    hosp_df = pd.read_excel('DataforMock.xlsx',sheet_name = 'Hospitals')
    
    
               
    drug_slang = st.selectbox('마약 관련 단어를 선택하시오.', drug_slang_list, help = '치안정책연구소에서 공개한 마약은어사전에 포함된 단어들입니다.')
    hosp = st.selectbox('병원', hosp_df, help = '치안정책연구소에서 공개한 마약은어사전에 포함된 단어들입니다.')
    
    m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))
    
    todf = pd.read_excel('DataforMock.xlsx',sheet_name = 'metrics')
    to = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Total Outstanding')]   
    ch = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Current Handover Average Mins')]   
    hl = todf[(todf['Hospital Attended']==hosp) & (todf['Metric']== 'Hours Lost to Handovers Over 15 Mins')]
    
    m1.write('')
    m2.metric(label ='전날 대비 증가량',value = str(int(to['Value']))+' 건', delta = str(int(to['Previous']))+', 전날 대비', delta_color = 'inverse')
    m3.metric(label ='가장 최근글',value = str(int(ch['Value']))+" 분 전", delta = str(int(ch['Previous']))+', 1분전', delta_color = 'inverse')
    m4.metric(label = '현재 위험도 가장 높은 글',value = str(int(hl['Value']))+" 건", delta = str(int(hl['Previous']))+', 3일전')
    m1.write('')
     
    # Number of Completed Handovers by Hour
    
    g1, g2, g3 = st.columns((1,1,1))
    
    fgdf = pd.read_excel('DataforMock.xlsx',sheet_name = 'Graph')
    
    fgdf = fgdf[fgdf['Hospital Attended']==hosp] 
    
    fig = px.bar(fgdf, x = 'Arrived Destination Resolved', y='Number of Handovers', template = 'seaborn')
    
    fig.update_traces(marker_color='#264653')
    
    fig.update_layout(title_text="Number of Completed Handovers by Hour",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g1.plotly_chart(fig, use_container_width=True) 
    
    # Predicted Number of Arrivals
    
    fcst = pd.read_excel('DataforMock.xlsx',sheet_name = 'Forecast')
    
    fcst = fcst[fcst['Hospital Attended']==hosp]
    
    fig = px.bar(fcst, x = 'Arrived Destination Resolved', y='y', template = 'seaborn')
    
    fig.update_traces(marker_color='#7A9E9F')
    
    fig.update_layout(title_text="Predicted Number of Arrivals",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g2.plotly_chart(fig, use_container_width=True)  
    
    # Average Completed Handover Duration by hour

    fig = px.bar(fgdf, x = 'Arrived Destination Resolved', y='Average Duration',color = "Average Duration", template = 'seaborn', color_continuous_scale=px.colors.diverging.Temps)
    
    fig.add_scatter(x=fgdf['Arrived Destination Resolved'], y=fgdf['Target'], mode='lines', line=dict(color="white"), name='Target')
    
    fig.update_layout(title_text="Average Completed Handover Duration by hour",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None, legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
    
    g3.plotly_chart(fig, use_container_width=True) 
      
    # Waiting Handovers table
    
    cw1, cw2 = st.columns((2.5, 1.7))
    
    whdf = pd.read_excel('DataforMock.xlsx',sheet_name = 'WaitingHandovers')
      
    colourcode = []
                             
    for i in range(0,9):
        colourcode.append(whdf['c'+str(i)].tolist())   
    
    whdf = whdf[['Hospital Attended ',	'Expected',	'Inbound ',	'Arrived ',	'Waiting',	'0 - 15 Mins',	'15 - 30 Mins ',	'30 - 60 Mins ',	'60 - 90 Mins',	'90 + Mins ',
]]
    
       
    fig = go.Figure(
            data = [go.Table (columnorder = [0,1,2,3,4,5,6,7,8,9], columnwidth = [30,10,10,10,10,15,15,15,15,15],
                header = dict(
                 values = list(whdf.columns),
                 font=dict(size=12, color = 'white'),
                 fill_color = '#264653',
                 line_color = '#4653FF',
                 align = ['left','center'],
                 #text wrapping
                 height=20
                 )
              , cells = dict(
                  values = [whdf[K].tolist() for K in whdf.columns], 
                  font=dict(size=12, color='black'),
                  align = ['left','center'],
                  fill_color = colourcode,
                  line_color = '#4653FF',
                  height=20))])
     
    fig.update_layout(title_text="Current Waiting Handovers",title_font_color = 'white',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)                                                           
        
    cw1.plotly_chart(fig, use_container_width=True)    
    
    # Current Waiting Table
    
    cwdf = pd.read_excel('DataforMock.xlsx',sheet_name = 'CurrentWaitingCallsigns')
    
    if hosp == 'All':
        cwdf = cwdf
    elif hosp != 'All':
        cwdf = cwdf[cwdf['Hospital Attended']==hosp]
    
    
    fig = go.Figure(
            data = [go.Table (columnorder = [0,1,2,3], columnwidth = [15,40,20,20],
                header = dict(
                 values = list(cwdf.columns),
                 font=dict(size=12, color = 'white'),
                 fill_color = '#264653',
                 align = 'left',
                 height=20
                 )
              , cells = dict(
                  values = [cwdf[K].tolist() for K in cwdf.columns], 
                  font=dict(size=12, color='black'),
                  align = 'left',
                  fill_color=colourcode,
                  height=20))]) 
        
    fig.update_layout(title_text="Current Waiting Callsigns",title_font_color = 'white',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=480)
        
    cw2.plotly_chart(fig, use_container_width=True)
       
with st.spinner('Report updated!'):
    time.sleep(1)     
    
# Performance Section  
    
with st.expander("Previous Performance"):
        
    hhc24 = pd.read_excel('DataforMock.xlsx',sheet_name = 'HospitalHandoversCompleted')  
    
    colourcode = []
                          
    for i in range(0,13):
        colourcode.append(hhc24['c'+str(i)].tolist())    
    
    hhc24 = hhc24[['Hospital Attended','Handovers','In Progress','Average','Hours Lost','0 to 15 mins','15 to 30 mins','30 to 60 mins','60 to 90 mins','90 to 120 mins','120 mins','% 15 Mins','% 30 Mins']]   
    
    fig = go.Figure(
            data = [go.Table (columnorder = [0,1,2,3,4,5,6,7,8,9,10,11,12], columnwidth = [18,12],
                header = dict(
                 values = list(hhc24.columns),
                 font=dict(size=11, color = 'white'),
                 fill_color = '#264653',
                 line_color = 'rgba(255,255,255,0.2)',
                 align = ['left','center'],
                 #text wrapping
                 height=20
                 )
              , cells = dict(
                  values = [hhc24[K].tolist() for K in hhc24.columns], 
                  font=dict(size=10),
                  align = ['left','center'],
                  fill_color = colourcode,
                  line_color = 'rgba(255,255,255,0.2)', 
                  height=20))])
     
    fig.update_layout(title_text="Hospital Handovers Completed in the Past 24 Hours",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=400)                                                               
    
    st.plotly_chart(fig, use_container_width=True)      
    
    p1,p2 = st.columns((3, 1.7))   
        
    #  Current Waiting Handovers
        
    hhc = pd.read_excel('DataforMock.xlsx',sheet_name = 'HospitalHandoverCompletedByHour')  
    
    hhc = hhc[hhc['Hospital Attended']==hosp]
    
    colourcode = []
                             
    for i in range(0,13):
        colourcode.append(hhc['c'+str(i)].tolist())    
    
    hhc = hhc[['dst','Handovers','In Progress','Average','Hours Lost','0 to 15 mins','15 to 30 mins','30 to 60 mins','60 to 90 mins','90 to 120 mins','120 mins','% 15 Mins','% 30 Mins']]
        
    fig = go.Figure(
            data = [go.Table (columnorder = [0,1,2,3,4,5,6,7,8,9,10,11,12], columnwidth = [18,12],
                header = dict(
                 values = list(hhc.columns),
                 font=dict(size=11, color = 'white'),
                 fill_color = '#264653',
                 line_color = 'rgba(255,255,255,0.2)',
                 align = ['left','center'],
                 #text wrapping
                 height=20
                 )
              , cells = dict(
                  values = [hhc[K].tolist() for K in hhc.columns], 
                  font=dict(size=10),
                  align = ['left','center'],
                  fill_color = colourcode,
                  line_color = 'rgba(255,255,255,0.2)',
                  height=20))])
     
    fig.update_layout(title_text="Hospital Handovers Completed by Hour",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=600)                                                               
    
    p1.plotly_chart(fig, use_container_width=True)  
    

    #  Longest Completed Handovers    
    
    lch = pd.read_excel('DataforMock.xlsx',sheet_name = 'LongestCompletedHandover')
        
    if hosp == 'All':
            lch = lch
    elif hosp != 'All':
        lch = lch[lch['Hospital Attended']==hosp]

    fig = go.Figure(
                data = [go.Table (columnorder = [0,1,2,3,4], columnwidth = [10,35,20,20,10],
                                  header = dict(
                                      values = list(lch.columns),
                                      font=dict(size=12, color = 'white'),
                                      fill_color = '#264653',
                                      align = 'left',
                                      height=20
                                          )
              , cells = dict(
                  values = [lch[K].tolist() for K in lch.columns], 
                  font=dict(size=11),
                  align = 'left',
                  fill_color='#F0F2F6',
                  height=20))])
        
    fig.update_layout(title_text="Longest Completed Handovers",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=600)
        
    p2.plotly_chart(fig, use_container_width=True)
        
        
        
        
        
        
        
        
        
        
