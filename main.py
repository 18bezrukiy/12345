from aiogram import executor
from google.cloud import dialogflow
import os
import handlers


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="df-web-ccgd-fbbbfb1958c1.json"
session_client = dialogflow.SessionsClient()
project_id = "df-web-ccgd"
session_id = 'sessions'
language_code = 'ru'
session = session_client.session_path(project_id, session_id)


async def on_startup(_):
    handlers.register_web_hand(dp)


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)