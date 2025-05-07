from automation.automator import start_task
from web.server import run_flask
import time

if __name__ == '__main__':
    print("프로그램을 실행합니다")
    print("작업을 수행합니다")
    run_flask()
    start_task()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("종료합니다.")


