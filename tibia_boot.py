import requests
import time
from datetime import datetime
import os

# CONFIGURAÇÕES (lidas do GitHub Actions via Secrets)
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]
DESTINO = os.environ["DESTINO"]

# Função para enviar mensagem no WhatsApp
def send_whatsapp_message(message):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": DESTINO,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)

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
            msg = f"Mundo voltou online! Boot detectado em: {boot_time}"
            print(msg)
            send_whatsapp_message(msg)
            break
        time.sleep(1)  # Checa a cada 1 segundo

if __name__ == "__main__":
    monitor_boot()
