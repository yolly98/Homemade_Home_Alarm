from CLI import CLI
from UDPServer import UDPServer
from AlarmManager import AlarmManager
from Cache import Cache
import threading
import time
from TelegramBotManager import TelegramBotManager
from WebServer import WebServer

PORT = 2390
KEEP_ALIVE_TIMER = 60 # 1 minute

def keep_alive_timer():
    while True:
        time.sleep(60)
        nodes = Cache.get_instance().get_nodes()
        if len(nodes) == 0:
            continue
        for node_id in nodes:
            node = nodes[node_id]
            node['status'] = 'dead'
            Cache.get_instance().add_node(node_id, node) 
            UDPServer.send('STATUS', node['addr'], node['port'])


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
    
    UDPServer.get_instance().init(PORT)

    udp_listener_thread = threading.Thread(target=UDPServer.get_instance().listen)
    msg_from_nodes_manager = threading.Thread(target=msg_from_node_handler)
    cli_manager_thread = threading.Thread(target=CLI.get_instance().listen)
    alarm_manager_thread = threading.Thread(target=AlarmManager.get_instance().alarm_player)
    keep_alive_thread = threading.Thread(target=keep_alive_timer)
    telegram_bot_manager = threading.Thread(target=TelegramBotManager.get_instance().telegram_bot())

    CLI.init()
    
    udp_listener_thread.start()
    msg_from_nodes_manager.start()
    cli_manager_thread.start()
    alarm_manager_thread.start()
    keep_alive_thread.start()
    telegram_bot_manager.start()

    WebServer.get_instance().listen("0.0.0.0", "9000")

    udp_listener_thread.join()
    msg_from_nodes_manager.join()
    cli_manager_thread.join()
    alarm_manager_thread.join()
    keep_alive_thread.join()
    telegram_bot_manager.join()