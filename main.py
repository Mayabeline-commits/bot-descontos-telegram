import os
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

print("--- INICIANDO SCRIPT COMPLETO ---")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")

def enviar_mensagem():
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN.strip()}/sendMessage"
        payload = {
            "chat_id": CHAT_ID.strip(),
            "text": "🚀 Bot de Ofertas Online ativado com sucesso!"
        }
        try:
            r = requests.post(url, json=payload, timeout=10)
            print(f"RESPOSTA TELEGRAM: Status {r.status_code} - {r.text}")
        except Exception as e:
            print(f"ERRO AO ENVIAR: {e}")
    else:
        print("FALTAM VARIAVEIS DE AMBIENTE!")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ativo e online!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"Servidor HTTP a correr na porta {port}")
    server.serve_forever()

# Envia a mensagem logo no arranque, numa thread separada
threading.Thread(target=enviar_mensagem, daemon=True).start()

# Inicia o servidor web obrigatório para o Render
run_server()
