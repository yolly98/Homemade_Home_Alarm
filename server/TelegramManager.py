import telegram
import telegram.ext
import requests
import re
from Cache import Cache

USER_FILE = "telegram_user_file.txt"
BOT_FILE = "telegram_bot_file.txt"
START = 0
COMMAND = 1

class TelegramManager:

    instance = None
    
    def __init__(self):
        user_file = open(USER_FILE,"r")
        bot_file = open(BOT_FILE,"r")

        self.bot_token = bot_file.readline()
        self.authorized_user = int(user_file.readline())

        user_file.close()
        bot_file.close()

        self.updater = telegram.ext.Updater(self.bot_token)
        self.dispatcher = self.updater.dispatcher
        pass

    @staticmethod
    def get_instance():
        if TelegramManager.instance is None:
            TelegramManager.instance = TelegramManager()
        return TelegramManager.instance
    
    def start(self, update_obj, context):
        #print("--- START state ---")
        update_obj.message.reply_text("Select a command",
            reply_markup=telegram.ReplyKeyboardMarkup([['ALARM', 'NODES'],[ 'STATUS', "RESET"]], one_time_keyboard=True)
        )
        return COMMAND
    
    def send_message_to_telegram(self, text):
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'

        params = {
            "chat_id": self.authorized_user,
            "text": text,
        }
        resp = requests.get(url, params=params)
        # Throw an exception if Telegram API fails
        resp.raise_for_status()

    def command(self, update_obj, context):
        #authentication
        user = update_obj.message.from_user['id']
        if self.authorized_user != user:
            update_obj.message.reply_text("user not authorized")
            #print("user " + user +" not authorized")
            return

        #switching to function
        #print("--- COMMAND state ---")
        if update_obj.message.text == 'ALARM':
            print('Received ALARM from telegram')
            pass

        elif update_obj.message.text == 'NODES':
            nodes = Cache.get_instance().get_nodes()
            for node_id in nodes:
                node = nodes[node_id]
                msg = f'-------------- \n node_id: {node_id} \n address: ({node["addr"]}, {node["port"]}) \n status: {node["status"]} \n alarm: {node["alarm"]} \n detection: {node["detection"]} \n --------------'
                self.send_message_to_telegram(msg)

        elif update_obj.message.text == 'STATUS':
            print('Received STATUS from telegram')
            pass

        elif update_obj.message.text == 'RESET':
            print('Received RESET from telegram')
            pass
        # return telegram.ext.ConversationHandler.END
        
    def telegram_bot(self):
        filter = re.compile(r'^(ALARM|NODES|STATUS|RESET)$', re.IGNORECASE)

        handler = telegram.ext.ConversationHandler(
            entry_points=[telegram.ext.CommandHandler('start', self.start)],
            states={
                    COMMAND: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(filter), self.command)],
            },
            fallbacks=[telegram.ext.CommandHandler('STATUS', self.start)],
        )

        self.dispatcher.add_handler(handler)
        self.updater.start_polling()
        #updater.idle()