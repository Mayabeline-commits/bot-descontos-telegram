import os
import asyncio
from flask import Flask
from threading import Thread
import telegram

# 1. Servidor Web com Flask para manter o Render ativo
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Descontos está online e a funcionar!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Função para enviar mensagem no Telegram
async def send_test_message():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")
    
    if not token or not channel_id:
        print("ERRO: TELEGRAM_BOT_TOKEN ou TELEGRAM_CHANNEL_ID não configurados!")
        return

    bot = telegram.Bot(token=token)
    
    mensagem = (
        "🔥 **Radar de Descontos Ativado!** 🔥\n\n"
        " O bot está configurado e pronto para postar as melhores ofertas da Shopee e Mercado Livre com os teus links de afiliado!\n\n"
        "⚡ Acompanha as promoções diárias aqui no canal!"
    )
    
    try:
        await bot.send_message(chat_id=channel_id, text=mensagem, parse_mode='Markdown')
        print("Mensagem enviada com sucesso para o canal!")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")

# 3. Inicialização Principal
if __name__ == "__main__":
    # Inicia o servidor web numa thread separada
    server_thread = Thread(target=run_flask)
    server_thread.daemon = True
    server_thread.start()
    
    # Envia a mensagem de teste ao iniciar
    asyncio.run(send_test_message())
    
    # Mantém o processo principal ativo
    server_thread.join()
