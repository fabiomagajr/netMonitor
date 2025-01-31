import requests
import socket
import time
import os
import getpass as gt
from datetime import datetime

API_IP = "seu_server"
API_URL = "http://seu_server:8000/update_status/"  # Substitua pelo endereço real da API
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
        # Cria um socket temporário para descobrir o IP real da máquina
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Usa o Google DNS como referência
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        log_error(f"Erro ao obter IP: {e}")
        return "0.0.0.0"


def send_status():
    hostname = socket.gethostname()
    ip = get_ip()
    user=gt.getuser()
    data = {"hostname": hostname, "user":user, "ip": ip, "ConnectionOK": True}
    
    try:
        response = requests.post(API_URL, json=data, timeout=5)
        response.raise_for_status()
        print(f"Conexão OK com a API: {API_IP}")
    except requests.RequestException as e:
        log_error(f"Erro ao enviar status: {e}")
    
if __name__ == "__main__":
    while True:
        send_status()
        time.sleep(CHECK_INTERVAL)
