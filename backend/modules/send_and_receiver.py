# モジュール定義
from flask import Flask, Response, request
from flask_cors import cross_origin, CORS
import time
import json
# メッセージ管理クラス


class sse_message():
    def __init__(self):
        self.message = ""

    def read(self):
        return self.message

    def send(self, value):
        self.message = value
# タスク管理クラス


class file_manager():
    tasklist = [
            {
                "projectName": "red",
                "fileName": "test.txt",
                "fileSize": "1234567890B",
                "uniqeId": "af5d656a-31be-4ec8-9039-56038b72c987",
                "progress": 0,
                "status": "CREATED"
            }]
    def __init__(self):
        self.tasklist = [
            {
                "projectName": "red",
                "fileName": "test.txt",
                "fileSize": "1234567890B",
                "uniqeId": "af5d656a-31be-4ec8-9039-56038b72c987",
                "progress": 0,
                "status": "CREATED"
            }]  # 下の例をそのまま挿入

    def add_task(self, info):  # 送信予定を送信
        self.tasklist.append(info)

    def get_task(self):
        return json.dumps(self.tasklist)

    # 該当するタスクのstatus変更　中断モジュールやfile_observerからの正常アクセスを意図
    def change_state(self, name, state):
        for i in self.tasklist:
            if i["fileName"] == name:
                i["status"] = state

    def send_error(self, name):  # 該当するタスクのstatus変更　一定時間を超えてファイルサイズが変更されていない際やハートビートの失敗などでの変更を意図
        for i in self.tasklist:
            if i["fileName"] == name:
                i["status"] = "error"

    def delete_task(self, name):  # change_stateの完了の表示後やsend_errorのエラー表示後の一定時間後に実行
        for i in self.tasklist:
            if i["fileName"] == name:
                del (i)


app = Flask(__name__)
CORS(app)

msg = sse_message()
file_manage = file_manager()
# SSE送信


@app.route("/get_task")
def sse():
    return Response(sse_make(), mimetype="text/event-stream")


def sse_make():
    while True:
        task_list = file_manage.get_task()
        msg.send(task_list)
        res = msg.read()
        yield f"data: {res}\n\n"
        time.sleep(1)


@app.route("/add_task", methods=["POST"])
def add():
    file_manage.add_task(request.json)
    # ここでタスクの追加処理を行うと想定
    x = file_manage.get_task()
    print(x)
    return x


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
