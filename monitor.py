import os, time, sqlite3, shutil
from collections import deque
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from encryption import compute_entropy
from config import TEST_DIR, DB_PATH, ENTROPY_THRESHOLD, RAPID_WRITE_WINDOW
from email_alert import send_alert

os.makedirs(TEST_DIR, exist_ok=True)

# =========================
# QUARANTINE SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUARANTINE_DIR = os.path.join(BASE_DIR, "quarantine")
os.makedirs(QUARANTINE_DIR, exist_ok=True)


def auto_quarantine(path):
    """Automatically move suspicious file to quarantine folder"""
    try:
        if os.path.exists(path):
            fname = os.path.basename(path)
            dest = os.path.join(
                QUARANTINE_DIR,
                str(int(time.time())) + "_" + fname
            )

            shutil.move(path, dest)
            print("[AUTO QUARANTINED]", dest)

            log_event("quarantined", dest)

    except Exception as e:
        print("Quarantine error:", e)


# =========================
# Init DB
# =========================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            timestamp TEXT,
            event_type TEXT,
            file_path TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_event(ev_type, path, details=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO events VALUES (?, ?, ?, ?)",
        (time.strftime("%Y-%m-%d %H:%M:%S"), ev_type, path, details)
    )
    conn.commit()
    conn.close()
    print(f"[{ev_type}] {path} {details}")


write_times = deque()


# =========================
# Handler
# =========================
class Handler(FileSystemEventHandler):

    def on_modified(self, event):
        if event.is_directory:
            return

        path = event.src_path

        try:
            ent = compute_entropy(path)
            log_event("modified", path, f"entropy={ent:.3f}")

            now = time.time()
            write_times.append(now)

            while write_times and now - write_times[0] > RAPID_WRITE_WINDOW:
                write_times.popleft()

            # -------------------------
            # HIGH ENTROPY → AUTO QUARANTINE
            # -------------------------
            if ent >= ENTROPY_THRESHOLD:
                log_event("suspicious_entropy", path, f"entropy={ent:.3f}")
                send_alert("AutoSec Alert", f"Suspicious file detected: {path}")
                auto_quarantine(path)   # ⭐ AUTO MOVE

            # -------------------------
            # RAPID WRITES → AUTO QUARANTINE
            # -------------------------
            if len(write_times) >= 10:
                log_event("high_write_rate", path, f"count={len(write_times)}")
                auto_quarantine(path)   # ⭐ AUTO MOVE

        except Exception as e:
            log_event("error", path, str(e))


# =========================
# Start Monitor
# =========================
def start_monitor():
    init_db()

    observer = Observer()
    handler = Handler()
    observer.schedule(handler, TEST_DIR, recursive=True)
    observer.start()

    print("[monitor] Watching:", TEST_DIR)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_monitor()
