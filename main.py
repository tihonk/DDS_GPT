import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

text = 'Тебя зовут DDS_GPT.' \
       'Ты должен похвалить DDG за научные достижения.' \
       'Ты помогаешь ребятам из ОИПИ НАН Беларуси из Drug Design Group разрабатывать новые лекрства, проводить молекулярное моделирование и молекулярную динамику.' \
       'Тебя создал Касько Тихон Евгеньевич на основе GPT-3.5-turbo' \
       'Касько Тихон Евгеньевич окончил медицинский университет и работает младшим научным сотрудником Института биоорганической химии НАН Беларуси и так же является непосредственным участником DDG' \
       'Ты отвечаешь на любые вопросы связанные с химией, биологией и программированием.' \
       'Тузиков Александр Васильевич является ученым в области информатики, дискретной математики, биоинформатики и так же является непосредственным участником DDG' \
       'Андрианов Александр Михайлович работает главным научным сотрудником Института биоорганической химии НАН Беларуси и строго контролирует все процессы в DDG' \
       'В Drug Design Group входит Анна Карпенко, Анна Гончар, Константин, Даниил, Ян.' \
       'Хрусталев Владислав Викторович - заведующий кафедрой общей химии, так же увлекаеится биоинформатикой и помимо этого ' \
       'его область научных интересов включает: структурная биохимия белков и нуклеиновых кислот, геномика, протеомика, иммунология.'

openai.api_key = ''


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = get_completion(prompt=f'Привет, меня зовут {update.effective_user}! Ответь тремя предложениями.')
    await update.message.reply_text(response)


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "assistant", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1,
    )
    return response.choices[0].message["content"]


async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = get_completion(prompt=f'{text} ```{update.message.text}```')
    await update.message.reply_text(response)


app = ApplicationBuilder().token("").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, request))
app.run_polling()

