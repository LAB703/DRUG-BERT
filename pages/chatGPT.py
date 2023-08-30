import streamlit as st
import title
import openai
import random

title.header()
# https://ask-my-pdf.streamlit.app/
#https://gpt4autocoder.streamlit.app/
# https://knowledgegpt.streamlit.app/
# https://langchain-chat-search.streamlit.app/
# https://langchain-quickstart.streamlit.app

with st.sidebar:
        st.markdown(
            "## 사용법\n"
            "1. 🔑 [OpenAI API key](https://platform.openai.com/account/api-keys)를 입력하세요. \n"  # noqa: E501
            "2. 📄 구글에서 크롤링된 파일을 입력하세요. \n"
            "3. 💬 실행을 누르세요.\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="OpenAI API key를 입력하세요. (sk-...)",
            help="여기에서 OpenAI API key를 발급받을 수 있습니다. https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY", ""),
                # os.environ.get("OPENAI_API_KEY", None)  # local       
        )

        st.session_state["OPENAI_API_KEY"] = api_key_input
        st.markdown("---")
        

openai_api_key = st.session_state.get("OPENAI_API_KEY")

st.write('---')
st.subheader('🆔 ChatGPT 아이디 식별기')

example_dict = { 1 : {
        "example" : '''
input : 엑스터시 팝니다,카톡【opn6】엑스터시 판매,엑스터시 구매,텔레【opn66】엑스터시 구입,엑스터시 판매사이트. 작성자. \n
output :
''',
"output" : 'opn66'},
        
2 : {
        "example" : '''
input : 정품엑스터시판매가격☆카톡:kodak8☆텔레그램:Komen68☆엑스터시온라인직구입방법 ... 엑스타시와 물뽕(GHB) ,고메요 ,프로포폴,졸피뎀 5종류 판매합니다. \n
output :
''',
"output" : 'Komen68'},

3 : {
        "example" : '''
input : People named 엑스터시 정품 판매 (( 3618.TK )) (( 카톡:app3 )) (( 라인:dpp3w )) (( 텔레그램:bby38 )) 지방 엑스터시 썰 엑스터시 직거래 구입 후기 ... \n
output :
''',
"output" : 'bby38'},
4 : {
        "example" : '''
input : 도리도리판매✩라인wto56✩텔레myy33✩카톡zcc38 라인wto56✩ ... 카톡zcc38✩ \n
output : 
''',
"output" : 'myy33'},
5 : {
        "example" : '''
input : 엑스터시 팝니다 (텔ㄹㅔ@fofoice) 엑스터시팝니다 엑스터시파는곳 ☎ 상담텔레 \n
output : 
''',
"output" : 'fofoice'},
}


prompt = '''
          prompt : 아래의 [extract]에서 텔레그램 아이디를 추출해야합니다. 예시는 [example]와 같습니다. 
        
          [example]
              input: 101서울떨액상구매(텔레@WICEW양산케타민팝니다ꗾ광주 ...
              output : WICEW
        
              input: 텔tktls44 #떨팝니다 #대마팝니다 #대마구하는방법 #허브
              output : tktls44
        
              input:떨팝니다텔레tyson779몰리판매작대기팝니다카톡tyson898 ...
              output : tyson779
        
              input: 떨 구입 (ㅌㄹ@zedice) 떨판매 떨구매 떨파는곳 떨팝니다 제더아이스 안녕하세요.각종 물건 판매하는 제더입니다. 안전을 최우선으로 2년동한 거래 ...
              output :  zedice
        
              input : 엑스터시구매-카톡:aky33 텔레:kid333 — '엑스터시,엑스터시판매,엑스터시파는곳,엑스터시사는
              output : kid333
        '''

with st.expander("사용된 프롬프트") :
        st.code(prompt)

def reset():
    st.session_state.selection = 'Please Select'

st.button('예시 문장 초기화', on_click=reset)
example_num = random.randrange(1,6)
st.text_area("", example_dict[example_num]['example'])
st.write('추출된 ID : :red[' + example_dict[example_num]['output'] + ']')


@st.cache_data(show_spinner=False)
def is_open_ai_key_valid(openai_api_key) -> bool:
    if not openai_api_key:
        st.warning("좌측에 OpenAI API key를 입력하시오!")
        return False
    try:
        prompt_content = f""" {prompt}
                
          [extract]
          {user_input}
        
          """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
              {"role": "user",
              "content": prompt_content}
            ]
          )
        print(response["choices"][0].message.content)
    except Exception as e:
        st.error(f"올바른 OpenAI API key가 아닙니다. 키를 재확인하세요.")
        # logger.error(f"올바른 OpenAI API key가 아닙니다. ")
        #     st.error(f"{e.__class__.__name__}: {e}")
        # logger.error(f"{e.__class__.__name__}: {e}")
        return False
    return True

user_input = st.text_area(
    "아이디를 식별하고 싶은 게시글을 입력하세요.",
    '''input :

    output :      
''')

if not user_input:
    st.stop()
else :
    is_open_ai_key_valid(openai_api_key)


# import os
# import openai

# #openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = "" 


extracts = [
   ''' input : 창원-액상떨팝니다->>텔LOVETHC <<-마리화나판매->>
  output : ''',

'''  input : v++〔강남떨[@SATAN114]강남떨있습니다강남떨팝니다ŧ ...
  output : ''',

  '''input : Shop for G액상떨 팝니다𓊆 Gochang11 𓊇액상떨 팝니다-액상떨팝니다-액상떨 판매-액상떨 팝니다-
  output : ''',

'''  input : 액상떨팝니다>>텔LOVETHC<<경기
  output : ''',

'''
input : 엑스터시 팝니다,카톡【opn6】엑스터시 판매,엑스터시 구매,텔레【opn66】엑스터시 구입,엑스터시 판매사이트. 작성자.
output :
''',

'''
input : 정품엑스터시판매가격☆카톡:kodak8☆텔레그램:Komen68☆엑스터시온라인직구입방법 ... 엑스타시와 물뽕(GHB) ,고메요 ,프로포폴,졸피뎀 5종류 판매합니다.
output :
''',
'''
input : People named 엑스터시 정품 판매 (( 3618.TK )) (( 카톡:app3 )) (( 라인:dpp3w )) (( 텔레그램:bby38 )) 지방 엑스터시 썰 엑스터시 직거래 구입 후기,LSD 먹이고 강간 ...
output :
''',
'''
input : 도리도리판매✩라인wto56✩텔레myy33✩카톡zcc38 라인wto56✩ ... 카톡zcc38✩
output : 
''',
'''
input : 엑스터시 팝니다 (텔ㄹㅔ@fofoice) 엑스터시팝니다 엑스터시파는곳 ☎ 상담텔레
output : 
'''

]
if openai_api_key:        
        for e in extracts :
          prompt = f"""
          prompt : 아래의 [extract]에서 텔레그램 아이디를 추출해야합니다. 예시는 [example]와 같습니다. 
        
          [example]
              input: 101서울떨액상구매(텔레@WICEW양산케타민팝니다ꗾ광주 ...
              output : WICEW
        
              input: 텔tktls44 #떨팝니다 #대마팝니다 #대마구하는방법 #허브
              output : tktls44
        
              input:떨팝니다텔레tyson779몰리판매작대기팝니다카톡tyson898 ...
              output : tyson779
        
              input: 떨 구입 (ㅌㄹ@zedice) 떨판매 떨구매 떨파는곳 떨팝니다 제더아이스 안녕하세요.각종 물건 판매하는 제더입니다. 안전을 최우선으로 2년동한 거래 ...
              output :  zedice
        
              input : 엑스터시구매-카톡:aky33 텔레:kid333 — '엑스터시,엑스터시판매,엑스터시파는곳,엑스터시사는
              output : kid333
        
        
          [extract]
          {e}
        
          """
          response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
              {"role": "user",
              "content": prompt}
            ]
          )
          print(response["choices"][0].message.content)
