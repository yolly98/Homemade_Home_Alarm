from CLI import CLI
from UDPServer import UDPServer
from AlarmManager import AlarmManager
from Cache import Cache
import threading
import time
from TelegramBotManager import TelegramBotManager
from WebServer import WebServer
from Protocols import Protocols
from Log import Log

PORT = 2390
KEEP_ALIVE_TIMER = 60 * 5 # 5 minutes
RESET_TIMER = 60 * 60 * 6 # 6 hours

def keep_alive_timer():
    while True:
        time.sleep(KEEP_ALIVE_TIMER)
        Protocols.keep_alive()

def rest_timer():
    while True:
        time.sleep(RESET_TIMER)
        TelegramBotManager.get_instance().send_message_to_telegram(f'reset protocol started')
        Protocols.reset()

def msg_from_node_handler():
    while True:
        msg = UDPServer.get_instance().get_message()
        msg = msg.split('/')
        addr = msg[0]
        port = int(msg[1])
        room = msg[2]
        id = msg[3]
        cmd = msg[4]
        node_id = f'/{room}/{id}'
        if cmd == 'INIT':
            node = {'addr': addr, 'port': port, 'room': room, 'id': id, 'status': 'alive', 'alarm': 'off', 'detection': False}
            Cache.get_instance().add_node(node_id, node)
            alarm_is_armed, detection = AlarmManager.get_instance().get_status()
            if alarm_is_armed:
                Protocols.send_cmd(node_id, 'ON')
            
        elif cmd == 'ON':
            node = {'addr': addr, 'port': port, 'room': room, 'id': id, 'status': 'alive', 'alarm': 'on', 'detection': False}
            Cache.get_instance().add_node(node_id, node)
        elif cmd == 'OFF':
            node = {'addr': addr, 'port': port, 'room': room, 'id': id, 'status': 'alive', 'alarm': 'off', 'detection': False}
            Cache.get_instance().add_node(node_id, node)
        elif cmd == 'DETECTED':
            node = {'addr': addr, 'port': port, 'room': room, 'id': id, 'status': 'alive', 'alarm': 'on', 'detection': True}
            Cache.get_instance().add_node(node_id, node)
            AlarmManager.get_instance().update_detections(node_id, True)
            TelegramBotManager.get_instance().send_message_to_telegram(f'[{node_id}] movement detected')
        elif cmd == 'FREE':
            node = {'addr': addr, 'port': port, 'room': room, 'id': id, 'status': 'alive', 'alarm': 'on', 'detection': False}
            Cache.get_instance().add_node(node_id, node)
            AlarmManager.get_instance().update_detections(node_id, False)
            TelegramBotManager.get_instance().send_message_to_telegram(f'[{node_id}] no movement detected')
        

if __name__ == '__main__':
    
    Log.get_instance().print('success', 'Server initialization started')
    UDPServer.get_instance().init(PORT)

    udp_listener_thread = threading.Thread(target=UDPServer.get_instance().listen)
    msg_from_nodes_manager = threading.Thread(target=msg_from_node_handler)
    cli_manager_thread = threading.Thread(target=CLI.get_instance().listen)
    alarm_manager_thread = threading.Thread(target=AlarmManager.get_instance().alarm_player)
    keep_alive_thread = threading.Thread(target=keep_alive_timer)
    reset_thread = threading.Thread(target=rest_timer)
    telegram_bot_manager = threading.Thread(target=TelegramBotManager.get_instance().telegram_bot())

    CLI.init()
    
    udp_listener_thread.start()
    msg_from_nodes_manager.start()
    cli_manager_thread.start()
    alarm_manager_thread.start()
    keep_alive_thread.start()
    reset_thread.start()
    telegram_bot_manager.start()

    Log.get_instance().print('success', 'Server threads started')

    WebServer.get_instance().listen("0.0.0.0", "9000")

    udp_listener_thread.join()
    msg_from_nodes_manager.join()
    cli_manager_thread.join()
    alarm_manager_thread.join()
    keep_alive_thread.join()
    reset_thread.join()
    telegram_bot_manager.join()