import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN, WEBPAGE_URL



# Esta funcion es la encargada de informar al usuario el funcionamiento del bot

async def start(update: Update, context: ContextTypes):
    await update.message.reply_text('Hola puedes mencionar mi nombre de usuario en un chat y te mandaré los precios en tiempo real de las divisas reflejados en el Toque' )


async def send_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if f'@{context.bot.username}' in update.message.text:
            response = requests.get(WEBPAGE_URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            sections = soup.find_all('div', {'class': 'content'})

            if sections:
                info = '\n\n'.join([section.get_text() for section in sections])

            await update.message.reply_text(info)
        else:
           await update.message.reply_text('Lo siento, en estos momentos no puedo mostrarte la información')
    except requests.RequestsException as e:
        await update.message.reply_text(f'Error de la web: {e}')
    except Exception as e:
        await update.message.reply_text('Ocurrio un error: {e}')


def main():
    application = ApplicationBuilder().token('7848607922:AAHm5Pq-Irlik_FR33javzoSIlj2yYNmgbw').build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_info ))

    application.run_polling()

if __name__== '__main__':
    main()
 

