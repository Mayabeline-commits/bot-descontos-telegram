import os
import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot do Telegram ativo!")

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

def enviar_mensagem():
    # Aguarda 3 segundos para garantir que o Render carregou as chaves
    time.sleep(3)
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHANNEL_ID")
    
    if not token or not chat_id:
        print(f"Erro: TOKEN ou CHAT_ID em falta! Token: {token}, Chat ID: {chat_id}")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "🚀 <b>Bot de Ofertas Online!</b>\nO robô foi configurado com sucesso e está ativo no Render.",
        "parse_mode": "HTML"
    }
    try:
        resposta = requests.post(url, data=payload)
        print("Resposta do Telegram:", resposta.json())
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

if __name__ == "__main__":
    print("Iniciando o servidor Web do Render...")
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    print("A enviar mensagem de teste para o Telegram...")
    # Dispara o envio da mensagem num canal separado para não bloquear o servidor
    threading.Thread(target=enviar_mensagem).daemon = True
    
    while True:
        time.sleep(60)
