from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import time
import threading
from fastapi.responses import HTMLResponse

app = FastAPI()

HOSTS_FILE = "hosts.json"
STATUS = {}  # Dicionário para armazenar o status dos hosts
CHECK_INTERVAL = 10  # Tempo para considerar um host como "Down"

class HostStatus(BaseModel):
    hostname: str
    ip: str
    ConnectionOK: bool

def load_hosts():
    try:
        with open(HOSTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_hosts(hosts):
    with open(HOSTS_FILE, "w") as file:
        json.dump(hosts, file, indent=4)

def monitor_hosts():
    while True:
        current_time = time.time()
        for host in STATUS.keys():
            if current_time - STATUS[host]["last_seen"] > CHECK_INTERVAL:
                STATUS[host]["status"] = "Down"
        time.sleep(10)

@app.post("/update_status/")
def update_status(data: HostStatus):
    hosts = load_hosts()
    if not any(h["hostname"] == data.hostname and h["ip"] == data.ip for h in hosts):
        hosts.append({"hostname": data.hostname, "ip": data.ip})
        save_hosts(hosts)
    
    STATUS[data.hostname] = {"ip": data.ip, "status": "OK" if data.ConnectionOK else "Down", "last_seen": time.time()}
    return {"message": "Status updated"}

@app.get("/status/", response_class=HTMLResponse)
def get_status():
    hosts = load_hosts()
    table_rows = "".join(
        f"<tr><td>{h['hostname']}</td><td>{h['ip']}</td><td style='color:{'green' if STATUS.get(h['hostname'], {}).get('status') == 'OK' else 'red'}'>{STATUS.get(h['hostname'], {}).get('status', 'Down')}</td></tr>"
        for h in hosts
    )
    return f"""
    <html>
    <head><meta http-equiv='refresh' content='10'></head>
    <body>
        <h2>Network Monitor</h2>
        <table border='1'>
            <tr><th>Hostname</th><th>IP</th><th>Connection</th></tr>
            {table_rows}
        </table>
    </body>
    </html>
    """

threading.Thread(target=monitor_hosts, daemon=True).start()
