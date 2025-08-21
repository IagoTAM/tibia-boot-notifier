import requests
import time
from datetime import datetime
import os

# CONFIGURAÇÕES (lidas do GitHub Actions via Secrets)
GOOGLE_SCRIPT_URL = os.environ["GOOGLE_SCRIPT_URL"]  # URL do Apps Script

# Função para enviar dados para o Google Sheets
def send_to_google_sheet(time_str, world="Venebra"):
    payload = {
        "time": time_str,
        "server": world
    }
    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload)
        if response.status_code == 200:
            print("Informação registrada no Google Sheets com sucesso.")
        else:
            print(f"Falha ao registrar no Sheets: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Erro ao enviar para o Sheets: {e}")

# Função para checar status do mundo
def check_world_status(world="Venebra"):
    url = f"https://api.tibiadata.com/v4/world/{world}"
    resp = requests.get(url).json()
    return resp["world"]["status"]

# Monitorar server boot
def monitor_boot():
    print("Aguardando server boot...")
    while True:
        status = check_world_status()
        if status == "online":
            boot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Mundo voltou online! Boot detectado em: {boot_time}")
            send_to_google_sheet(boot_time)
            break
        time.sleep(1)  # Checa a cada 1 segundo

if __name__ == "__main__":
    monitor_boot()
