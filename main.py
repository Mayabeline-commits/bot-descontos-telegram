import os
import requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Descontos ativo!", 200

def enviar_mensagem_direta():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")
    
    print(f"--- INICIANDO ENVIO ---")
    print(f"Token presente: {bool(token)}")
    print(f"Channel ID: {channel_id}")
    
    if not token or not channel_id:
        print("ERRO: Variáveis de ambiente ausentes!")
        return

    # Limpa espaços em branco extras se houver
    token = token.strip()
    channel_id = channel_id.strip()

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": "🔥 Radar de Descontos Ativado! O bot está conectado e pronto para postar ofertas."
    }

    try:
        resposta = requests.post(url, data=payload, timeout=10)
        dados = resposta.json()
        print(f"RESPOSTA DO TELEGRAM: {dados}")
    except Exception as e:
        print(f"ERRO DE CONEXAO: {e}")

# Executa o envio imediatamente ao carregar o arquivo
enviar_mensagem_direta()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
