import telegram
import telegram.ext
import requests
import re
from Cache import Cache
from Protocols import Protocols

USER_FILE = "telegram_user_file.txt"
BOT_FILE = "telegram_bot_file.txt"
START = 0
COMMAND = 1
BOT_ENABLE = False

class TelegramBotManager:

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
        if TelegramBotManager.instance is None:
            TelegramBotManager.instance = TelegramBotManager()
        return TelegramBotManager.instance
    
    def start(self, update_obj, context):
        if BOT_ENABLE == False:
            return
        #print("--- START state ---")
        update_obj.message.reply_text("Select a command",
            reply_markup=telegram.ReplyKeyboardMarkup([['ALARM ON', 'ALARM OFF'],[ 'STATUS', "KEEP ALIVE"], ["RESET", "END BOT"]], one_time_keyboard=True)
        )
        return COMMAND
    
    def send_message_to_telegram(self, text):
        if BOT_ENABLE == False:
            return
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'

        params = {
            "chat_id": self.authorized_user,
            "text": text,
        }
        resp = requests.get(url, params=params)
        # Throw an exception if Telegram API fails
        resp.raise_for_status()

    def command(self, update_obj, context):
        if BOT_ENABLE == False:
            return
        #authentication
        user = update_obj.message.from_user['id']
        if self.authorized_user != user:
            update_obj.message.reply_text("user not authorized")
            return

        #switching to function
        #print("--- COMMAND state ---")

        if update_obj.message.text == 'ALARM ON':
            Protocols.alarm_on()
            self.send_message_to_telegram('ALARM ARMED')

        elif update_obj.message.text == 'ALARM OFF':
            Protocols.alarm_off()
            self.send_message_to_telegram('ALARM DISARMED')

        elif update_obj.message.text == 'STATUS':
            status = Protocols.status()
            self.send_message_to_telegram(f"Alarm: {status['alarm']}")
            self.send_message_to_telegram(f"Alerted: {status['alerted']}")
            nodes = status['nodes']
            if len(nodes) == 0:
                self.send_message_to_telegram('No nodes connected')
            else:
                for node_id in nodes:
                    node = nodes[node_id]
                    msg = f'-------------- \n node_id: {node_id} \n address: ({node["addr"]}, {node["port"]}) \n status: {node["status"]} \n alarm: {node["alarm"]} \n detection: {node["detection"]} \n --------------'
                    self.send_message_to_telegram(msg)

        elif update_obj.message.text == 'KEEP ALIVE':
            Protocols.keep_alive()
            self.send_message_to_telegram('KEEP ALIVE protocol started')

        elif update_obj.message.text == 'RESET':
            Protocols.reset()
            self.send_message_to_telegram('RESET protocol started')

        elif update_obj.message.text == 'END BOT':
            self.send_message_to_telegram('Telegram bot disabled (enter "/start" to restart it)')
            return telegram.ext.ConversationHandler.END
        
    def telegram_bot(self):
        if BOT_ENABLE == False:
            return
        filter = re.compile(r'^(ALARM ON|ALARM OFF|STATUS|KEEP ALIVE|RESET|END BOT)$', re.IGNORECASE)

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