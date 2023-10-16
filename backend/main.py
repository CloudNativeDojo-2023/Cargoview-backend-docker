import threading
from modules.file_observer import start_monitoring
from modules.send_and_receiver import app, msg
if __name__ == "__main__":
    # Flaskアプリケーションを起動するスレッド
    app_thread = threading.Thread(target=app.run, kwargs={
                                  "host": '0.0.0.0', "port": 5000})
    app_thread.start()
    # ファイル監視を起動するスレッド
    file_thread = threading.Thread(target=start_monitoring, args=("./upload",))
    file_thread.start()

