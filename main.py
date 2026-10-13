import os
import requests
import time

# O código lê o Token e o Canal que configuramos nas Environment Variables do Render
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")

def enviar_mensagem(texto):
    if not TOKEN or not CHAT_ID:
        print("Erro: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHANNEL_ID não definidos.")
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

if _name_ == "_main_":
    print("Bot de Descontos iniciado no Render...")
    
    # Envia uma mensagem de teste no seu canal assim que o robô liga
    enviar_mensagem("🚀 <b>Bot de Ofertas Online!</b>\nO robô foi configurado com sucesso e está rodando no Render.")
    
    # Mantém o robô ativo em segundo plano
    while True:
        time.sleep(60)
