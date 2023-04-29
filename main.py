import openai
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

initial_text_ru = 'Ответь в стиле, словно ты мой друг из Drug Disign Group из ОИПИ Академии Наук Беларуси.'
initial_text_en = 'Answer in style, as if you are my friend from the Drug Design Group ' \
                  'from the UIPI of the Academy of Sciences of Belarus.'

openai.api_key = ''


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = gpt_message(content='Привет!', user=update.effective_user)
    await update.message.reply_text(response)


async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = gpt_message(content=update.message.text, user=update.effective_user)
    await update.message.reply_text(response)


def gpt_message(content: str, user):
    start_message = initial_text_ru if re.search('[а-яА-Я]', content) else initial_text_en
    full_text = get_completion(f'{start_message} {content}')
    first_later = full_text[0].lower()
    rest_text = full_text[1:]
    return f'{user.first_name}, {first_later}{rest_text}'


app = ApplicationBuilder().token().build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, request))
app.run_polling()

