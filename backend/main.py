import threading
from modules.file_observer import start_monitoring
from modules.send_and_receiver import app, msg
import json
import time
if __name__ == "__main__":
    # Flaskアプリケーションを起動するスレッド
    app_thread = threading.Thread(target=app.run, kwargs={
                                  "host": '0.0.0.0', "port": 5000})
    app_thread.start()

    # ファイル監視を起動するスレッド
    file_thread = threading.Thread(target=start_monitoring, args=("./upload",))
    file_thread.start()
    file_thread2 = threading.Thread(target=start_monitoring, args=("./upload2",))
    file_thread2.start()
    file_thread3 = threading.Thread(target=start_monitoring, args=("./upload3",))
    file_thread3.start()

