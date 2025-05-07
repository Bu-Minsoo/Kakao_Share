from bs4 import BeautifulSoup as bs
import threading
from automation import driver
import time
from ai import gpt

import requests

# BASE_URL = "https://www.ibabynews.com"
# URL = [
#     {"category": "육아/교육", "link": "/news/articleList.html?sc_section_code=S1N4&view_type=sm"},
#     {"category": "여성/가족", "link": "/news/articleList.html?sc_section_code=S1N8&view_type=sm"},
#     {"category": "오피니언", "link": "/news/articleList.html?sc_section_code=S1N6&view_type=sm"},
# ]

BASE_URL = "https://m.entertain.naver.com/now"

is_chrome_init = False
index = 0

# URL = f"{BASE_URL}/news/articleList.html?sc_sub_section_code=S2N1&view_type=sm"

news_list = {}

def start_crawling():
    task_thread = threading.Thread(target=crawl_lists)
    task_thread.daemon = True  # 프로그램 종료 시 서버도 종료되도록 설정
    task_thread.start()

# www.ibabynews.com 크롤링
# def crawl_lists():
#     global URL, BASE_URL, index
#     news_list.clear()
#     log.append_log("크롤링을 시작합니다.")
#     response = requests.get(BASE_URL + URL[index]['link'])
#     print(f"======= request url = [{BASE_URL + URL[index]['link']}] =======================")
#     gemini.init_gemini()
#
#     if response.status_code == 200:  # 정상 응답 반환 시 아래 코드블록 실행
#         soup = bs(response.content, 'html.parser')  # 응답 받은 HTML 파싱
#         lists = soup.find_all("div", {"class": 'list-block'})
#
#         # 차라리 여기서 3개를 추출하는 것이 빠를지도
#         # 아직 컨셉이 잡힌 것이 없으니 놔두자
#         for i in range(3):
#             article_info = {}
#
#             # 링크 추출
#             a_tag = lists[i].find("a", href=True)
#             article_url = BASE_URL + a_tag["href"]
#             article_info["url"] = article_url
#
#             # 날짜 추출
#             date_div = lists[i].find("div", class_="list-dated")
#             tmp_text = date_div.get_text(strip=True)
#             date_text = tmp_text.split("|")[2].strip().split(" ")[0]
#             article_info["date"] = date_text
#
#             # 이미지 소스 추출
#             # img_tag = lists[i].find("img", src=True)
#             # print(f"img_tag: {img_tag}")
#             # img_url = BASE_URL + img_tag["src"][1:]
#             # print(f"img_url: {img_url}")
#             # article_info["img"] = img_url
#
#             # 제목 추출
#             # 쓰레드 동기화가 걸린다면, 이건 나중에 추가하는 것도 고려해볼 만 함
#             # 빠른 테스트를 위해 제목 고정
#             # 원래는 이거로 동적 생성
#             paragraph = get_paragraph(article_url)
#             title = gemini.get_response(paragraph)
#             article_info["title"] = title
#             # article_info["title"] = "title"
#
#             response = requests.get(article_url)
#             if response.status_code == 200:
#                 soup_img = bs(response.content, 'html.parser')
#                 lists_img = soup_img.find_all("div", {"class": 'IMGFLOATING'})
#                 print(len(lists_img))
#
#                 if len(lists_img) == 0:
#                     article_info["img"] = None
#                 else:
#                     img_tag = lists_img[0].find("img", src=True)
#                     img_url = BASE_URL + img_tag["src"]
#                     article_info["img"] = img_url
#                     print(img_url)
#
#
#             # description 은 "육아"로 고정
#             article_info["description"] = URL[index]['category']
#
#             news_list.append(article_info)
#     # print(json.dumps(news_list, indent=4, ensure_ascii=False))
#     log.append_log("크롤링이 완료되었습니다.")
#     index += 1


# 네이버 뉴스 크롤링

# 네이버 뉴스 크롤링 (링크만 가져와서 건네주기)
def crawl_lists():
    global BASE_URL, is_chrome_init
    news_list.clear()
    if is_chrome_init is False:
        driver.init_chrome()
        is_chrome_init = True
    driver.get_url(BASE_URL)

    time.sleep(2)

    soup = bs(driver.get_pagesource(), 'lxml')

    lists = soup.find_all("li", class_=lambda x: x and 'NewsItem_news_item__' in x)
    body_lists = soup.find_all("p", class_=lambda x: x and 'NewsItem_description__' in x)

    a_tag_list = [li.find("a", href=True)["href"] for li in lists if li.find("a", href=True)]

    body_link_list = [[body_lists[i].text[:250], a_tag_list[i]] for i in range(25)]
    print(body_link_list)

    # with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #
    #     # 헤더 (선택 사항)
    #     writer.writerow(['Column1', 'Column2'])
    #
    #     # 배열의 각 행을 CSV에 작성
    #     for row in csv_file_list:
    #         writer.writerow(row)



    # gemini.init_gemini()
    # news_list['link'] = gemini.get_related_url(a_tag_list)

    if a_tag_list:
        print(len(a_tag_list))
        news_list['link'] =gpt.get_related_url(body_link_list)


        time.sleep(3)

        # gpt 확인 후 다음 해제
        driver.get_url(news_list['link'])
        body = driver.get_body()

        # title, body = gemini.get_title_body(body)
        title, body = gpt.get_title_body(body)
        news_list['title'] = title
        news_list['body'] = body

    print(f"a_tag_list 길이: {len(a_tag_list)}")
    print(f"선택된 링크: {news_list.get('link')}")
    print(f"생성된 타이틀: {news_list.get('title')}")

    #     for i in range(3):
    #         article_info = {}
    #
    #         # 링크 추출
    #         a_tag = lists[i].find("a", href=True)
    #         article_url = BASE_URL + a_tag["href"]
    #         article_info["url"] = article_url
    #
    #         # 날짜 추출
    #         date_div = lists[i].find("div", class_="list-dated")
    #         tmp_text = date_div.get_text(strip=True)
    #         date_text = tmp_text.split("|")[2].strip().split(" ")[0]
    #         article_info["date"] = date_text
    #
    #         # 이미지 소스 추출
    #         # img_tag = lists[i].find("img", src=True)
    #         # print(f"img_tag: {img_tag}")
    #         # img_url = BASE_URL + img_tag["src"][1:]
    #         # print(f"img_url: {img_url}")
    #         # article_info["img"] = img_url
    #
    #         # 제목 추출
    #         # 쓰레드 동기화가 걸린다면, 이건 나중에 추가하는 것도 고려해볼 만 함
    #         # 빠른 테스트를 위해 제목 고정
    #         # 원래는 이거로 동적 생성
    #         paragraph = get_paragraph(article_url)
    #         title = gemini.get_response(paragraph)
    #         article_info["title"] = title
    #         # article_info["title"] = "title"
    #
    #         response = requests.get(article_url)
    #         if response.status_code == 200:
    #             soup_img = bs(response.content, 'html.parser')
    #             lists_img = soup_img.find_all("div", {"class": 'IMGFLOATING'})
    #             print(len(lists_img))
    #
    #             if len(lists_img) == 0:
    #                 article_info["img"] = None
    #             else:
    #                 img_tag = lists_img[0].find("img", src=True)
    #                 img_url = BASE_URL + img_tag["src"]
    #                 article_info["img"] = img_url
    #                 print(img_url)
    #
    #
    #         # description 은 "육아"로 고정
    #         article_info["description"] = URL[index]['category']
    #
    #         news_list.append(article_info)
    # # print(json.dumps(news_list, indent=4, ensure_ascii=False))
    # log.append_log("크롤링이 완료되었습니다.")
    # index += 1

def get_paragraph(article_url):
    response = requests.get(article_url)
    article_text = ""  # 기사 내용을 저장할 변수 초기화

    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        paragraphs = soup.find_all('p')

        for p in paragraphs:
            if p is not None:
                text = p.get_text(strip=True)
                if text is not None and len(text) > 0:
                    # print(text)
                    article_text += text + "\n"  # 추출된 텍스트를 변수에 추가

        return article_text if len(article_text) > 0 else None  # 내용이 있으면 반환, 없으면 None 반환
    return None


