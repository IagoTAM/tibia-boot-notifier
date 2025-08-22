import requests
import os
from datetime import datetime

GOOGLE_SCRIPT_URL = os.environ.get("GOOGLE_SCRIPT_URL")
if not GOOGLE_SCRIPT_URL:
    raise ValueError("O segredo GOOGLE_SCRIPT_URL não está definido!")

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
payload = {
    "time": now,
    "server": "Venebra-Test"
}

try:
    response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
    if response.status_code == 200:
        print(f"Teste enviado com sucesso: {payload}")
    else:
        print(f"Falha ao enviar: {response.status_code}, {response.text}")
except Exception as e:
    print(f"Erro ao enviar para o Sheets: {e}")
