from automation.automator import start_task
from web.server import start_server
import time

if __name__ == '__main__':
    print("프로그램을 실행합니다")
    start_server()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("종료합니다.")


