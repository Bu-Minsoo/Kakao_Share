from automation.automator import start_task
from flask import Flask, render_template
import os
import flask
from automation import crawling as cr
app = Flask(__name__)

import time

@app.route('/', methods=["GET", "HEAD"])
def share():
    if flask.request.method == "HEAD":
        return "", 200  # 헬스 체크용 빈 응답

    print("랜더링을 시작합니다.")

    title = cr.news_list['title'].strip().replace('"', '').replace("'", "")
    body = cr.news_list['body'].strip().replace('"', '').replace("'", "")

    link = cr.news_list['link']

    return render_template('text.html', app_key='c03ce9560aa54cba52b9fc2c4db6b3aa',
                           title=title, body=body, link=link)


if __name__ == '__main__':
    print("프로그램을 실행합니다")
    start_task()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
    print("작업을 수행합니다")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("종료합니다.")


