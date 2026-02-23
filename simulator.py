# simulator.py
# Safe simulator: creates backups and then writes random bytes and renames files to .locked inside TEST_DIR.
import os, shutil, random, time
from config import TEST_DIR, BACKUP_DIR, SIM_PID_FILE

def safe_backup():
    if os.path.exists(TEST_DIR):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        dest = os.path.join(BACKUP_DIR, f"backup_{int(time.time())}")
        shutil.copytree(TEST_DIR, dest)
        print("[sim] backup created:", dest)

def random_bytes(n):
    return bytes(random.getrandbits(8) for _ in range(n))

def create_initial(num=20):
    os.makedirs(TEST_DIR, exist_ok=True)
    for i in range(num):
        p = os.path.join(TEST_DIR, f"file_{i}.txt")
        with open(p, 'wb') as f:
            f.write(b"Hello world\n" * 3)

def simulate(num=20, size=1024, pause=0.15):
    safe_backup()
    create_initial(num)
    for i in range(num):
        p = os.path.join(TEST_DIR, f"file_{i}.txt")
        try:
            with open(p, 'ab') as f:
                f.write(random_bytes(size))
            os.rename(p, p + '.locked')
        except Exception as e:
            print("sim error:", e)
        time.sleep(pause)
    print("[sim] done")

def write_pid():
    with open(SIM_PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

def remove_pid():
    try:
        if os.path.exists(SIM_PID_FILE):
            os.remove(SIM_PID_FILE)
    except:
        pass

if __name__ == '__main__':
    write_pid()
    try:
        simulate(num=30)
    finally:
        remove_pid()
