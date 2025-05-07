import os
import threading

from flask.cli import load_dotenv

from automation import driver
import time

from automation.driver import check_login_needed
from automation import crawling
from apscheduler.schedulers.background import BackgroundScheduler

from web import server

if_login_success = False
is_chrome_init = False
# is_server_init = False

def start_task():
    # def run_task():
    #     set_task()  # 여기에 작업 내용을 직접 넣으면 됩니다

    set_task()

    # 이후 4시간마다 실행
    scheduler = BackgroundScheduler()
    scheduler.add_job(set_task, 'interval', minutes=2)
    scheduler.start()
    # def run_task():
    #     set_task()
    #
    # task_thread = threading.Thread(target=run_task, daemon=False)
    # task_thread.start()
    #
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(
    #     lambda: threading.Thread(target=run_task, daemon=False).start(),
    #     'interval',
    #     hours=4
    # )
    # scheduler.start()



def set_task():
    global if_login_success, is_server_init
    load_dotenv()

    # 크롤링 시작 & news_list(crawling.py)에 저장
    crawling.crawl_lists()
    # if is_server_init is False:
    #     server.start_server()
    #     is_server_init = True
    enter_url()

    # 로그인 화면이 뜨는지 확인
    if check_login_needed():
        driver.execute_login(os.getenv("ID"), os.getenv("PW"))
        # driver.execute_login(data[0], data[1])

        # 못 찾을 경우 2초마다 확인
        while True:
            time.sleep(2)
            if driver.check_login_done():
                break

    # 로그인 후 버튼 비활성화
    driver.ready_chatroom()
    if driver.is_chatroom_exist(os.getenv("ROOM")):
        driver.click_chatroom()
        driver.click_share()
        driver.close_popup()
        driver.deactivate_popup()

def enter_url():
    # global is_chrome_init
    #
    # if is_chrome_init is False:
    #     wx.CallAfter(log.append_log, "크롬을 초기화합니다.")
    #     driver.init_chrome()
    #     wx.CallAfter(log.append_log, "크롬 초기화 완료")
    #     is_chrome_init = True
    url = os.getenv("APP_BASE_URL", "http://localhost:9005")
    driver.get_url(url)
    time.sleep(2)
    driver.click_share_button()
    time.sleep(2)

    # 팝업창 전환 후 로그인
    driver.activate_popup()

    # 이건 메인문에서 실행
    # driver.execute_login()

    # 작업 수행 버튼 다시 활성화 하고, 로그인 인증 진행

# 로그인 했을 시 보여야 하는 요소가 뜨는지 확인

