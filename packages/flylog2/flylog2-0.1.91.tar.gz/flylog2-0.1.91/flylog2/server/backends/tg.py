import telegram

class TelegramBackend(object):

    def __init__(self, token):
        self.bot = telegram.Bot(token=token)

    def emit(self, title, content, chat_id):
        text = '\n\n'.join([title, content])
        try:
            self.bot.send_message(chat_id=chat_id, text=text, timeout=5)
        except:
            return False
        return True
