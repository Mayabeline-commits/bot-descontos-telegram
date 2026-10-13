import os
import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Pega as variáveis configuradas no Render
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Mini-servidor Web para o Render não desligar o robô
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot do Telegram ativo!")

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

def enviar_mensagem(texto):
    if not TOKEN or not CHAT_ID:
        print("Erro: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHANNEL_ID nao definidos.")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "HTML"
    }
    try:
        resposta = requests.post(url, data=payload)
        print("Mensagem enviada com sucesso!")
        return resposta.json()
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

# Execução direta sem verificação de traços
print("Iniciando o servidor Web do Render...")
server_thread = threading.Thread(target=run_web_server)
server_thread.daemon = True
server_thread.start()

print("Bot de Descontos iniciado no Render...")
enviar_mensagem("🚀 <b>Bot de Ofertas Online!</b>\nO robô foi configurado com sucesso e está ativo no Render.")

while True:
    time.sleep(60)
