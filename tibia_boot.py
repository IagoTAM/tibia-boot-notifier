import requests
  
import time
  
from datetime import datetime, time as dtime
  
from zoneinfo import ZoneInfo  # para trabalhar com fuso horário
  
import os
  

  
# CONFIGURAÇÕES
  
GOOGLE_SCRIPT_URL = os.environ.get("GOOGLE_SCRIPT_URL")
  
if not GOOGLE_SCRIPT_URL:
  
    raise ValueError("O segredo GOOGLE_SCRIPT_URL não está definido!")
  

  
WORLD = "Venebra"
  
CHECK_INTERVAL = 3  # segundos entre cada checagem
  
MAX_ATTEMPTS = 1200  # número máximo de tentativas (ex: 1200 x 3s = ~1h)
  
TZ = ZoneInfo("America/Sao_Paulo")  # GMT-3 com horário de verão ajustado
  
SERVER_SAVE_TIME = dtime(5, 0, 30)  # 05:00:30 no fuso definido
  

  
# Função para enviar dados para o Google Sheets
  
def send_to_google_sheet(time_str, world=WORLD):
  
    payload = {
  
        "time": time_str,
  
        "server": world
  
    }
  
    try:
  
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=15)
  
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
  
        resp = requests.get(url, timeout=3)
  
        resp.raise_for_status()
  
        data = resp.json()
  
        return data["world"]["status"]
  
    except Exception as e:
  
        print(f"Erro ao consultar API do Tibia: {e}")
  
        return "offline"  # assume offline se falhar
  

  
# Monitorar server boot (espera cair -> depois voltar -> só registra após 05:00 GMT-3)
  
def monitor_boot():
  
    print(f"Aguardando server boot de {WORLD} (horário GMT-3)...")
  
    attempts = 0
  
    saw_offline = False  # flag: já detectou mundo offline?
  

  
    while attempts < MAX_ATTEMPTS:
  
        status = check_world_status()
  
        now_dt = datetime.now(TZ)  # pega horário no GMT-3
  
        now = now_dt.strftime("%H:%M:%S")
  

  
        if not saw_offline:
  
            # Antes do server save: esperar o mundo cair
  
            if status == "offline":
  
                saw_offline = True
  
                print(f"{now} - {WORLD} caiu (offline detectado).")
  
            else:
  
                print(f"{now} - {WORLD} ainda online (antes do SS). Tentativa {attempts+1}/{MAX_ATTEMPTS}")
  
        else:
  
            # Depois do server save: esperar o mundo voltar online
  
            if status == "online" and now_dt.time() >= SERVER_SAVE_TIME:
  
                print(f"Mundo voltou online! Boot detectado em: {now}")
  
                send_to_google_sheet(now)
  
                return
  
            elif status == "online":
  
                print(f"{now} - {WORLD} voltou online, mas antes das 05:00 → ignorado.")
  
            else:
  
                print(f"{now} - {WORLD} ainda offline (aguardando boot). Tentativa {attempts+1}/{MAX_ATTEMPTS}")
  

  
        attempts += 1
  
        time.sleep(CHECK_INTERVAL)
  

  
    print(f"Máximo de tentativas atingido ({MAX_ATTEMPTS}). Script encerrado.")
  

  
if __name__ == "__main__":
  
    monitor_boot()
