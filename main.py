import os
import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

print("--- INICIANDO BOT DO TELEGRAM ---")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")

if TOKEN:
    TOKEN = TOKEN.strip()
if CHAT_ID:
    CHAT_ID = CHAT_ID.strip()

print(f"DEBUG: CHAT_ID carregado -> '{CHAT_ID}'")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot ativo!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Inicia servidor em segundo plano
server_thread = threading.Thread(target=run_web_server)
server_thread.daemon = True
server_thread.start()

time.sleep(2)

def enviar_mensagem_teste():
    if TOKEN and CHAT_ID:
        print(f"Enviando mensagem para: {CHAT_ID}...")
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": "🚀 <b>Bot de Ofertas Online!</b>\nO robô foi configurado com sucesso!",
            "parse_mode": "HTML"
        }
        try:
            resposta = requests.post(url, json=payload, timeout=10)
            res_json = resposta.json()
            print("--- RESPOSTA DO TELEGRAM ---")
            print(res_json)
            print("----------------------------")
        except Exception as e:
            print(f"Erro na requisição HTTP: {e}")
    else:
        print("ERRO: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHANNEL_ID não estão preenchidos no Render!")

# Dispara a mensagem
enviar_mensagem_teste()

# Mantém o robô rodando
while True:
    time.sleep(60)
