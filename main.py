import os
import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

print("--- INICIANDO BOT DO TELEGRAM ---")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")

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

# Inicia o servidor web em background para o Render não dar erro de porta
server_thread = threading.Thread(target=run_web_server)
server_thread.daemon = True
server_thread.start()

# Aguarda 2 segundos para o servidor estabilizar
time.sleep(2)

# Envia a mensagem de teste
if TOKEN and CHAT_ID:
    print(f"Tentando enviar mensagem para {CHAT_ID}...")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🚀 <b>Bot de Ofertas Online!</b>\nO robô foi configurado com sucesso e está ativo no Render.",
        "parse_mode": "HTML"
    }
    try:
        resposta = requests.post(url, data=payload)
        res_json = resposta.json()
        print("Resposta do Telegram:", res_json)
        if not res_json.get("ok"):
            print("ERRO DO TELEGRAM:", res_json.get("description"))
    except Exception as e:
        print(f"Erro na requisição: {e}")
else:
    print("ERRO: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHANNEL_ID não configurados!")

# Mantém o processo ativo
while True:
    time.sleep(60)
   
