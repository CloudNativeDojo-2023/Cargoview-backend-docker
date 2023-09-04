# モジュール定義
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import threading
from modules.send_and_receiver import msg,file_manage
# ファイル監視開始関数(origin)
def start_monitoring(path):
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

# ファイル状態検知クラス
class FileHandler(FileSystemEventHandler):
    def __init__(self):
        self.file_size = {}
        self.file_mtime = {}
        self.timer_threads = {}

    def on_created(self, event):
        # ファイルが作成された時に実行されるコード
        self.file_size[event.src_path] = 0
        self.file_mtime[event.src_path] = time.time()
        file_name = event.src_path.split("/")[-1]
        file_manage.change_state(file_name,"IN_PROGRESS")
        print(f"ファイルが送信開始されました: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            current_size = os.path.getsize(file_path)
            self.file_size[file_path] = current_size#状態を更新
            self.file_mtime[event.src_path] = time.time()#変更時間を取得
            
            if file_path in self.file_size and current_size == self.file_size[file_path]:
                if file_path in self.timer_threads:  # 既存のタイマースレッドが存在する場合
                    self.timer_threads[file_path].cancel()  # 既存のタイマースレッドをキャンセルする

                # 新しいタイマースレッドを作成して開始する
                timer_thread = threading.Timer(5, self.execute_after_timer, args=(file_path,))
                self.timer_threads[file_path] = timer_thread
                timer_thread.start()
                print("start")
                msg.send(f"ファイルが送信中です {current_size}")
            else:
                self.file_size[file_path] = current_size
                self.file_mtime[file_path] = time.time()
    
    def execute_after_timer(self, file_path):
        # タイマー経過後に実行する処理
        print("end")
        print(f"5秒経過したファイルは {file_path} です")
        msg.send("ファイルが送信完了されました")
        del self.timer_threads[file_path]

    def on_deleted(self, event):
        # ファイルが削除された時に実行されるコード
        if event.src_path in self.file_size:
            del self.file_size[event.src_path]
            del self.file_mtime[event.src_path]
            print(f"ファイルが削除されました: {event.src_path}")
