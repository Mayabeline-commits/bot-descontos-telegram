import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Descontos Automático ativo!", 200

# LISTA DE OFERTAS AUTOMÁTICAS
OFERTAS = [
    {
        "titulo": "🔥 Fone de Ouvido Bluetooth Sem Fio TWS",
        "preco_antigo": "R$ 89,90",
        "preco_promocao": "R$ 39,90",
        "link": "https://shope.ee/SEU_LINK_DE_AFILIADO_1",
        "imagem": "https://m.media-amazon.com/images/I/61-+QzZ3pEL._AC_SL1000_.jpg"
    },
    {
        "titulo": "⚡ Fritadeira Eletrica Air Fryer 4L",
        "preco_antigo": "R$ 399,00",
        "preco_promocao": "R$ 249,00",
        "link": "https://mercadolivre.com/sec/SEU_LINK_DE_AFILIADO_2",
        "imagem": "https://m.media-amazon.com/images/I/61NfIqfJ4tL._AC_SL1000_.jpg"
    }
]

def publicar_oferta(oferta):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")

    if not token or not channel_id:
        print("ERRO: Variaveis de ambiente nao encontradas.")
        return

    mensagem = f"{oferta['titulo']}\n\n❌ De: {oferta['preco_antigo']}\n✅ Por: *{oferta['preco_promocao']}*\n\n🛒 *Compre aqui:* {oferta['link']}"

    url = f"https://api.telegram.org/bot{token.strip()}/sendPhoto"
    payload = {
        "chat_id": channel_id.strip(),
        "photo": oferta["imagem"],
        "caption": mensagem,
        "parse_mode": "Markdown"
    }

    try:
        resposta = requests.post(url, data=payload, timeout=10)
        print(f"Publicacao enviada: {resposta.json()}")
    except Exception as e:
        print(f"Erro ao publicar: {e}")

def agendador():
    time.sleep(10)
    indice = 0
    while True:
        oferta_atual = OFERTAS[indice]
        print(f"Publicando oferta: {oferta_atual['titulo']}")
        publicar_oferta(oferta_atual)
        indice = (indice + 1) % len(OERTAS) if 'OERTAS' in locals() else (indice + 1) % len(OFERTAS)
        time.sleep(300)

if __name__ == "__main__":
    thread_agendador = Thread(target=agendador)
    thread_agendador.daemon = True
    thread_agendador.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
