from datetime import datetime, timedelta

import telegram

from server import settings
from traceback import print_exc

from server.helpers.report import generate_chart_report

if settings.TELEGRAM_TOKEN:
    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)


def handle_message(request):
    message = telegram.Update.de_json(
        request.get_json(force=True), bot
    ).effective_message
    if message is None:
        return "ok"

    chat_id = message.chat.id
    msg_id = message.message_id
    text = message.text.encode("utf-8").decode()

    try:
        if text == "/start":
            do_welcome(chat_id, msg_id)

        elif text.startswith("/chart"):
            do_send_chart(text, chat_id, msg_id)

    except Exception:
        bot.sendMessage(
            chat_id=chat_id,
            text="😔 Mi dispiace, si è verificato un errore. Riprova più tardi.",
        )
        print_exc()

    return "ok"


def set_webhook():
    s = bot.setWebhook(f"{settings.APP_BASE_URL}{settings.TELEGRAM_TOKEN}")
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


def do_welcome(chat_id, msg_id):
    bot.sendMessage(chat_id=chat_id, text="TODO welcome", reply_to_message_id=msg_id)


def do_send_chart(text: str, chat_id, msg_id):
    # TODO based on text, compute date from
    date_from = datetime.today() - timedelta(days=7)
    date_to = datetime.today()

    file_path = generate_chart_report(date_from, date_to)
    bot.send_photo(chat_id, photo=open(file_path, "rb"), reply_to_message_id=msg_id)
