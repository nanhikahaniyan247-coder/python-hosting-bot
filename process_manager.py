import subprocess, psutil, time, threading, json, os

DATA = "data.json"

def load():
    with open(DATA) as f:
        return json.load(f)

def save(d):
    with open(DATA,"w") as f:
        json.dump(d,f,indent=2)

def start_process(file):
    p = subprocess.Popen(["python", file])
    d = load()
    d[file] = p.pid
    save(d)

def stop_process(file):
    d = load()
    pid = d.get(file)
    if pid and psutil.pid_exists(pid):
        psutil.Process(pid).kill()
    d.pop(file,None)
    save(d)

def is_running(file):
    d = load()
    pid = d.get(file)
    return pid and psutil.pid_exists(pid)

def auto_restart():
    while True:
        d = load()
        for f,pid in list(d.items()):
            if not psutil.pid_exists(pid):
                start_process(f)
        time.sleep(5)

threading.Thread(target=auto_restart,daemon=True).start()
