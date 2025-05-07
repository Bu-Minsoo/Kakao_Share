# from flask import Flask, render_template
# import threading, os
# from automation import crawling as cr
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Kakao_Share/
# TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')  # Kakao_Share/templates
#
# app = Flask(__name__, template_folder=TEMPLATE_DIR)
#
# def start_server():
#     print("서버를 실행합니다...")
#     flask_thread = threading.Thread(target=run_flask)
#     flask_thread.daemon = True  # 프로그램 종료 시 서버도 종료되도록 설정
#     flask_thread.start()
#
# def run_flask():
#     app.run(debug=True, port=9005, use_reloader=False)
#
# # @app.route('/')
# # def share():
# #     summaries = cr.news_list
# #     contents = []
# #     default_image = 'http://k.kakaocdn.net/dn/bDPMIb/btqgeoTRQvd/49BuF1gNo6UXkdbKecx600/kakaolink40_original.png'
# #     default_link = 'https://developers.kakao.com'
# #
# #
# #     print(json.dumps(summaries, indent=4, ensure_ascii=False))
# #
# #     for i in range(3):
# #         contents.append({
# #             'title': summaries[i]["title"],
# #             'description': summaries[i]["description"], # 필요에 따라 변경
# #             'imageUrl': summaries[i]["img"] if summaries[i]["img"] else default_image,
# #             'link': {
# #                 'mobileWebUrl': summaries[i]["url"],
# #                 'webUrl': summaries[i]["url"],
# #             },
# #         })
# #         print(contents[i])
# #         print("=" * 30)
# #
# #
# #     # summaries 리스트의 길이가 3보다 작으면 기본 contents를 채워줍니다.
# #     while len(contents) < 3:
# #         contents.append({
# #             'title': '기사 제목 없음',
# #             'description': '내용 없음',
# #             'imageUrl': default_image,
# #             'link': {
# #                 'mobileWebUrl': default_link,
# #                 'webUrl': default_link,
# #             },
# #         })
# #
# #     return render_template('shared.html', app_key='c03ce9560aa54cba52b9fc2c4db6b3aa', contents=contents)
#
# # @app.route('/')
# # def share():
# #     return render_template('share.html', app_key='c03ce9560aa54cba52b9fc2c4db6b3aa')
# #
# # @app.route('/')
# # def share():
# #     return render_template('feed.html', app_key='c03ce9560aa54cba52b9fc2c4db6b3aa')
#
# @app.route('/')
# def share():
#     # raw_body = cr.news_list['title'] + "\n" + cr.news_list['body']
#     # body = raw_body.replace('"', '').replace("'", "")
#     # raw_body = "test"
#
#     title = cr.news_list['title'].strip().replace('"', '').replace("'", "")
#     body = cr.news_list['body'].strip().replace('"', '').replace("'", "")
#
#     # formatted_link = "https://localhost:9005/proxy?target=" + cr.news_list['link'].replace('https', 'http')
#     # formatted_link = cr.news_list['link'].replace('https', 'http')
#     link = cr.news_list['link']
#     print("link = " + link)
#
#     # original_link = cr.news_list['link']
#
#     # 🔧 여기서 링크를 인코딩해서 프록시 주소로 변환
#     # encoded_link = urllib.parse.quote(original_link, safe='')
#     # link = f'https://proxy.liyao.space/{encoded_link}'
#     # print("encoded_link = ", encoded_link)
#     # print("link = ", link)
#
#     return render_template('text.html', app_key='c03ce9560aa54cba52b9fc2c4db6b3aa',
#                            title=title, body=body, link=link)

from automation import crawling as cr
from flask import Flask, render_template
from flask_apscheduler import APScheduler
import os, time
from automation import crawling, driver
from automation.driver import check_login_needed

class Config:
    SCHEDULER_API_ENABLED = True  # (선택) API를 통해 스케줄러 관리 가능

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()

@app.route('/')
def share():
    title = cr.news_list['title'].strip().replace('"', '').replace("'", "")
    body = cr.news_list['body'].strip().replace('"', '').replace("'", "")
    link = cr.news_list['link']
    # 이건 기존처럼 렌더링
    return render_template('text.html', app_key='c03ce9560aa54cba52b9fc2c4db6b3aa',
                            title=title, body=body, link=link)

# 🧠 이게 우리가 주기적으로 실행하고 싶은 작업
def scheduled_task():
    print("=== 자동 작업 실행 ===")
    crawling.crawl_lists()

    driver.get_url("http://localhost:9005")
    time.sleep(2)
    driver.click_share_button()
    time.sleep(2)
    driver.activate_popup()

    if check_login_needed():
        driver.execute_login(os.getenv("ID"), os.getenv("PW"))
        while not driver.check_login_done():
            time.sleep(2)

    driver.ready_chatroom()
    if driver.is_chatroom_exist(os.getenv("ROOM")):
        driver.click_chatroom()
        driver.click_share()
        driver.close_popup()
        driver.deactivate_popup()

def start_server():
    scheduler.init_app(app)
    scheduler.start()

    # 첫 실행도 하고 주기적 실행도 설정
    scheduled_task()  # 수동 첫 실행
    scheduler.add_job(id='Scheduled Task', func=scheduled_task, trigger='interval', hours=4)

    app.run(debug=True, port=9005, use_reloader=False)