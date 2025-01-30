import requests
import socket
import time
import os
from datetime import datetime

API_URL = "http://seu_servidor:8000/update_status/"  # Substitua pelo endereço real da API
ERROR_LOG_DIR = "ErrorLogs"
CHECK_INTERVAL = 5  # Tempo entre cada envio de status

def log_error(message):
    if not os.path.exists(ERROR_LOG_DIR):
        os.makedirs(ERROR_LOG_DIR)
    
    log_filename = f"{ERROR_LOG_DIR}/ErrorLog{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(log_filename, "a") as log_file:
        log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        log_error(f"Erro ao obter IP: {e}")
        return "0.0.0.0"

def send_status():
    hostname = socket.gethostname()
    ip = get_ip()
    data = {"hostname": hostname, "ip": ip, "ConnectionOK": True}
    
    try:
        response = requests.post(API_URL, json=data, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        log_error(f"Erro ao enviar status: {e}")
    
if __name__ == "__main__":
    while True:
        send_status()
        time.sleep(CHECK_INTERVAL)
