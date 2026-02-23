import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEST_DIR = os.path.join(BASE_DIR, "test_dir")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
SIM_PID_FILE = os.path.join(BASE_DIR, "simulator.pid")

DB_PATH = os.path.join(BASE_DIR, "events.db")

ENTROPY_THRESHOLD = 7.5
RAPID_WRITE_WINDOW = 2