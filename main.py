from automation.automator import start_task
from web.server import start_server

if __name__ == '__main__':
    print("프로그램을 실행합니다")
    start_server()
    print("작업을 시작합니다.")
    start_task()


