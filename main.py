import os
import requests
from flask import Flask

app = Flask(__name__)

# LISTA DE OFERTAS
OFERTAS = [
    {
        "titulo": "🔥 Fone de Ouvido Bluetooth TWS",
        "preco_antigo": "R$ 89,90",
        "preco_promocao": "R$ 39,90",
        "link": "https://shope.ee/SEU_LINK_DE_AFILIADO_1"
    },
    {
        "titulo": "⚡ Fritadeira Eletrica Air Fryer 4L",
        "preco_antigo": "R$ 399,00",
        "preco_promocao": "R$ 249,00",
        "link": "https://mercadolivre.com/sec/SEU_LINK_DE_AFILIADO_2"
    }
]

@app.route('/')
def home():
    return "Bot de Descontos ativo!", 200

def enviar_oferta_inicial():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")

    if not token or not channel_id:
        print("ERRO: Variaveis ausentes")
        return

    oferta = OFERTAS["titulo": "🔥 NOME DO TEU PRODUTO AQUI",
        "preco_antigo": "R$ 100,00",
        "preco_promocao": "R$ 49,90",
        "link": "https://shope.ee/TEU_LINK_DE_AFILIADO"]
    mensagem = (
        f"{oferta['titulo']}\n\n"
        f"❌ De: {oferta['preco_antigo']}\n"
        f"✅ Por: {oferta['preco_promocao']}\n\n"
        f"🛒 Compre aqui: {oferta['link']}"
    )

    url = f"https://api.telegram.org/bot{token.strip()}/sendMessage"
    payload = {
        "chat_id": channel_id.strip(),
        "text": mensagem
    }

    try:
        res = requests.post(url, data=payload, timeout=10)
        print(f"RESPOSTA DA OFERTA: {res.json()}")
    except Exception as e:
        print(f"ERRO AO ENVIAR MENSAGEM: {e}")

# Dispara a oferta IMEDIATAMENTE ao iniciar
enviar_oferta_inicial()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
