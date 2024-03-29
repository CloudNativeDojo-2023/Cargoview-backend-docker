import threading
from modules.file_observer import start_monitoring
from modules.send_and_receiver import app, msg
import json
import time
if __name__ == "__main__":
    # Flaskアプリケーションを起動するスレッド
    app_thread = threading.Thread(target=app.run, kwargs={"host":'0.0.0.0',"port": 5000})
    app_thread.start()

    # ファイル監視を起動するスレッド
    file_thread = threading.Thread(target=start_monitoring, args=("/upload",))
    file_thread.start()

    lists = [
        {
            "projectName": "プロジェクトA",
            "ipAddr": "192.168.0.201",
            "fileSize": "10GB",
            "fileName": "【カット処理済み】〇〇プロジェクト.mp4",
            "progress": 0,
            "status": "IN_PROGRESS",
            "icon": "/userIcons/user01.png"
        },
    ]

    # 1秒ごとにメッセージを更新する
    """while True:
        time.sleep(1)
        for i in range(1, 100):
            lists[0]["progress"] = i
            res = json.dumps(lists)
            msg.send(res)
            time.sleep(0.5)
        
        lists[0]["status"] = "COMPLETED"
        res = json.dumps(lists)
        msg.send(res)"""
