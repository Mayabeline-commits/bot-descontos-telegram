import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(_name_)

@app.route('/')
def home():
    return "Bot de Descontos Automático ativo!", 200

# LISTA DE OFERTAS AUTOMÁTICAS
# Substitui os links de exemplo pelos teus links de afiliado da Shopee / Mercado Livre!
OFERTAS = [
    {
        "titulo": "🔥 Fone de Ouvido Bluetooth Sem Fio TWS",
        "preco_antigo": "R$ 89,90",
        "preco_promocao": "R$ 39,90",
        "link": "https://shope.ee/SEU_LINK_DE_AFILIADO_1",
        "imagem": "https://m.media-amazon.com/images/I/61-+QzZ3pEL._AC_SL1000_.jpg"
    },
    {
        "titulo": "⚡ Fritadeira Elétrica Air Fryer 4L",
        "preco_antigo": "R$ 399,00",
        "preco_promocao": "R$ 249,00",
        "link": "https://mercadolivre.com/sec/SEU_LINK_DE_AFILIADO_2",
        "imagem": "https://m.media-amazon.com/images/I/61NfIqfJ4tL._AC_SL1000_.jpg"
    },
    {
        "titulo": "📱 Carregador Rápido USB-C 20W",
        "preco_antigo": "R$ 49,90",
        "preco_promocao": "R$ 19,90",
        "link": "https://shope.ee/SEU_LINK_DE_AFILIADO_3",
        "imagem": "https://m.media-amazon.com/images/I/51IInN+M4nL._AC_SL1000_.jpg"
    }
]

def publicar_oferta(oferta):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")

    if not token or not channel_id:
        print("ERRO: Variáveis de ambiente não encontradas.")
        return

    mensagem = (
        f"{oferta['titulo']}\n\n"
        f"❌ De: {oferta['preco_antigo']}\n"
        f"✅ Por: {oferta['preco_promocao']}\n\n"
        f"🛒 Compre aqui: {oferta['link']}"
    )

    url = f"https://api.telegram.org/bot{token.strip()}/sendPhoto"
    payload = {
        "chat_id": channel_id.strip(),
        "photo": oferta["imagem"],
        "caption": mensagem,
        "parse_mode": "Markdown"
    }

    try:
        resposta = requests.post(url, data=payload, timeout=10)
        print(f"Publicação enviada: {resposta.json()}")
    except Exception as e:
        print(f"Erro ao publicar: {e}")

def agendador():
    # Espera 10 segundos antes da primeira postagem
    time.sleep(10)
    
    indice = 0
    while True:
        oferta_atual = OFERTAS[indice]
        print(f"Publicando oferta: {oferta_atual['titulo']}")
        publicar_oferta(oferta_atual)

        # Avança para a próxima oferta da lista
        indice = (indice + 1) % len(OFERTAS)

        # Intervalo em segundos entre as postagens (exemplo: 3600s = 1 hora)
        # Para testes iniciais, está configurado para postar a cada 300 segundos (5 minutos)
        time.sleep(300)

if _name_ == "_main_":
    # Inicia o agendador de ofertas numa thread em segundo plano
    thread_agendador = Thread(target=agendador)
    thread_agendador.daemon = True
    thread_agendador.start()

    # Inicia o servidor web do Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
