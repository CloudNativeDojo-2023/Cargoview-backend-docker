# モジュール定義
from flask import Flask, Response , request
from flask_cors import cross_origin,CORS
import time

# メッセージ管理クラス
class sse_message():
    def __init__(self):
        self.message = ""
    def read(self):
        return self.message
    def send(self,value):
        self.message = value
#タスク管理クラス
class file_manager():
    def __init__(self):
        self.tasklist = [{
            "projectName": "プロジェクトA",
            "ipAddr": "192.168.0.201",
            "fileSize": "10GB",
            "fileName": "test",
            "progress": 0,
            "status": "NOT",
            "icon": "/userIcons/user01.png"
        }]#下の例をそのまま挿入
    def add_task(self,info):#送信予定を送信
        self.tasklist.append(info)
    def get_task(self):
        return self.tasklist
    def change_state(self,name,state):#該当するタスクのstatus変更　中断モジュールやfile_observerからの正常アクセスを意図
        for i in self.tasklist:
            if i["fileName"] == name:
                i["status"] = state
    def send_error(self,name):#該当するタスクのstatus変更　一定時間を超えてファイルサイズが変更されていない際やハートビートの失敗などでの変更を意図
        for i in self.tasklist:
            if i["fileName"] == name:
                i["status"] = "error"
    def delete_task(self,name):#change_stateの完了の表示後やsend_errorのエラー表示後の一定時間後に実行
        for i in self.tasklist:
            if i["fileName"] == name:
                del(i)        
                
"""
送信されるリストの形式　アイコンについては除外してもよいかも
lists = {
            "projectName": "プロジェクトA",
            "ipAddr": "192.168.0.201",
            "fileSize": "10GB",
            "fileName": "【カット処理済み】〇〇プロジェクト.mp4",
            "progress": 0,
            "":
            "status": "IN_PROGRESS",
            "icon": "/userIcons/user01.png"
        }
"""
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
    app.run(debug=True,host="0.0.0.0")

