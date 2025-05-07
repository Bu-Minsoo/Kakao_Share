import google.generativeai as genai

gemini_key = "AIzaSyDo6wlM9Q6SFKS-rpHoS_sJQabVt9OEDnI"
# gemini_key = "AIzaSyA1eJ6rzCHxHzrLoLb7OvjamMjmo9XzdY8"
# gemini_key = "AIzaSyDjTR8G2RpGYH58e3dtAD4cuUYn2JzWkdU"
model = None

def init_gemini():
    global model
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

def get_related_url(urls):
    global model

    response = model.generate_content(f"""
            이건 50개의 뉴스 링크들이야.
            
            {urls}
            
            이 중에서 '아기, 교육, 키즈 에이전시'와 관련 있는 기사 url 하나만 뽑아서 출력해 줘.
            출력은 다른 말 필요 없이 url만 건네줘""")
    return response.text

def get_title_body(body):
    global model

    response = model.generate_content(f"""
            여기 뉴스 기사가 있어.
            
            {body}
            
            이 기사를 읽고 제목을 15자가 넘지 않게, 본문은 150자 이내로 요약해 줘.
            그리고 문장 요약할 때 특수문자는 , . 이 두개만 써야 해. 다른 건 절대 쓰지 마
            물음표, 느낌표도 절대 쓰지마 제발 하지 말라는건 하지 마.
            쌍따옴표("), 홑따옴표(') 이 두개도 절대 쓰지 마
            그리고 제목과 본문 사이에 [!@#$%]라는 문자열을 넣어줘
            """)
    result = response.text.split("[!@#$%]")
    return result[0].strip(), result[1].strip()

def get_response(p, max_retries=5):
    """
    Fetch a response using the Gemini API with retry logic
    implemented to handle rate limits (429 errors).
    """
    global model

    # Request to the Gemini API
    response = model.generate_content(
        f"""
        이건 내가 스크랩한 기사야. 다음 기사를 제목으로 쓸 수 있도록 15자가 넘지 않게 간결하게 요약해 줘

        {p}
        """
    )
    print("[response] = " + response.text)
    return response.text



# def get_response(p):
#     global model
#     response = None
#     while response is None:
#         response = model.generate_content(f"""
#                     이건 내가 스크랩한 기사야. 다음 기사를 제목으로 쓸 수 있도록 15자가 넘지 않게 간결하게 요약해 줘
#
#                     {p}""")
#
#     return response.text


