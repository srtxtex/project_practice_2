from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import rag_lm

# возьмем переменные окружения из .env
load_dotenv()

# загружаем значеняи из файла .env
TOKEN = os.environ.get("TOKEN")


# функция команды /start
async def start(update, context):
  await update.message.reply_text('Привет! Это бот пекGPT.')

# функция для текстовых сообщений
async def text(update, context):
    # использование update
    print('-------------------')
    # print(f'update: {update}')
    print(f'date: {update.message.date}')
    print(f'id message: {update.message.message_id}')
    print(f'name: {update.message.from_user.first_name}')
    print(f'user.id: {update.message.from_user.id}')

    topic = update.message.text
    print(f'text: {topic}')

    chat_type = update.message.chat.type

    reply_text, gpt_message_content = rag_lm.answer_user_question(topic)


    await update.message.reply_text(f'{reply_text}')

    print(f'reply_text:\n{reply_text}')
    print('-------------------')


def main():
    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен..!')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()

    print('Бот остановлен..!')


if __name__ == "__main__":
    main()
