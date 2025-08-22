import requests
import time
from datetime import datetime
import os

# CONFIGURAÇÕES
GOOGLE_SCRIPT_URL = os.environ.get("GOOGLE_SCRIPT_URL")
if not GOOGLE_SCRIPT_URL:
    raise ValueError("O segredo GOOGLE_SCRIPT_URL não está definido!")

WORLD = "Venebra"
CHECK_INTERVAL = 1  # segundos entre cada checagem
MAX_ATTEMPTS = 3600  # número máximo de tentativas (ex: 3600 x 1s = ~1h)

# Função para enviar dados para o Google Sheets
def send_to_google_sheet(time_str, world=WORLD):
    payload = {
        "time": time_str,
        "server": world
    }
    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=1)
        if response.status_code == 200:
            print(f"Informação registrada no Google Sheets: {time_str}")
        else:
            print(f"Falha ao registrar no Sheets: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Erro ao enviar para o Sheets: {e}")

# Função para checar status do mundo
def check_world_status(world=WORLD):
    url = f"https://api.tibiadata.com/v4/world/{world}"
    try:
        resp = requests.get(url, timeout=1)
        resp.raise_for_status()
        data = resp.json()
        return data["world"]["status"]
    except Exception as e:
        print(f"Erro ao consultar API do Tibia: {e}")
        return "offline"  # assume offline se falhar

# Monitorar server boot
def monitor_boot():
    print(f"Aguardando server boot de {WORLD}...")
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        status = check_world_status()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if status == "online":
            print(f"Mundo voltou online! Boot detectado em: {now}")
            send_to_google_sheet(now)
            return
        else:
            print(f"{now} - {WORLD} ainda offline. Tentativa {attempts+1}/{MAX_ATTEMPTS}")
        attempts += 1
        time.sleep(CHECK_INTERVAL)
    print(f"Máximo de tentativas atingido ({MAX_ATTEMPTS}). Script encerrado.")

if __name__ == "__main__":
    monitor_boot()

