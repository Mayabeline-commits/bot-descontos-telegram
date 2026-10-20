import os
import asyncio
from flask import Flask
import telegram

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Descontos ativo!", 200

async def send_welcome():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")
    if token and channel_id:
        try:
            bot = telegram.Bot(token=token)
            await bot.send_message(
                chat_id=channel_id,
                text="🔥 **Radar de Descontos Ativado!** 🔥\n\nO bot está configurado e pronto para postar as melhores ofertas da Shopee e Mercado Livre com os teus links de afiliado!",
                parse_mode='Markdown'
            )
            print("Mensagem enviada com sucesso!")
        except Exception as e:
            print(f"Erro Telegram: {e}")

# Dispara a mensagem assim que o arquivo é carregado pelo Render
try:
    asyncio.run(send_welcome())
except Exception as e:
    print(f"Erro asyncio: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
