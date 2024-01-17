from AlarmManager import AlarmManager
from Cache import Cache
from UDPServer import UDPServer
from Log import Log
import os
import signal

class Protocols: 
    def __init__(self):
        pass

    def alarm_on():
        Log.get_instance().print('cmd', 'Protocol Started: ALARM ON')
        AlarmManager.get_instance().armAlarm()
        nodes = Cache.get_instance().get_nodes()
        for node_id in nodes:
            node = nodes[node_id]
            UDPServer.send('ON', node['addr'], node['port'])

    def alarm_off():
        Log.get_instance().print('cmd', 'Protocol Started: ALARM OFF')
        AlarmManager.get_instance().disarmAlarm()
        nodes = Cache.get_instance().get_nodes()
        for node_id in nodes:
            node = nodes[node_id]
            UDPServer.send('OFF', node['addr'], node['port'])

    def send_cmd(node_id, cmd):
        Log.get_instance().print('cmd', f'Protocol Started: SEND {cmd} to {node_id}')
        node = Cache.get_instance().get_node(node_id)
        if node is None:
            return False
        else:
            UDPServer.send(cmd, node['addr'], node['port'])
        return True

    def keep_alive():
        Log.get_instance().print('cmd', 'Protocol Started: KEEP ALIVE')
        nodes = Cache.get_instance().get_nodes()
        if len(nodes) == 0:
            return False
        else:
            for node_id in nodes:
                node = nodes[node_id]
                node['status'] = 'dead'
                Cache.get_instance().add_node(node_id, node) 
                UDPServer.send('STATUS', node['addr'], node['port'])
        return True

    def reset():
        Log.get_instance().print('cmd', 'Protocol Started: RESET')
        nodes = Cache.get_instance().get_nodes()
        if len(nodes) == 0:
            return False
        else:
            for node_id in nodes:
                node = nodes[node_id]
                UDPServer.send('RESET', node['addr'], node['port'])
        return True

    def status():
        Log.get_instance().print('cmd', 'Protocol Started: STATUS')
        status = dict()
        isArmed, alarmStatus = AlarmManager.get_instance().get_status()
        if isArmed:
            status['alarm'] = 'armed'
        else:
            status['alarm'] = 'disarmed'
        if alarmStatus:
            status['alerted'] = 'yes'
        else:
            status['alerted'] = 'no'
        status['nodes'] = Cache.get_instance().get_nodes()
        return status
    
    def remove(node_id):
        Log.get_instance().print('cmd', f'Protocol Started: REMOVE {node_id}')
        return Cache.get_instance().remove_node(node_id)
    
    def assign_alias(node_id, alias):
        Log.get_instance().print('cmd', 'Protocol Started: ALIAS')
        node = Cache.get_instance().get_node(node_id)
        if node is None:
            return False
        node['alias'] = alias
        Cache.get_instance().add_node(node_id, node)
        return True
    
    def exit():
        Log.get_instance().print('cmd', 'Protocol Started: EXIT')
        try:
            os.kill(os.getpid(), signal.SIGTERM)
        except:
            pass