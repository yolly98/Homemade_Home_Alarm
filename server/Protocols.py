from AlarmManager import AlarmManager
from Cache import Cache
from UDPServer import UDPServer

class Protocols: 
    def __init__(self):
        pass

    def alarm_on():
        AlarmManager.get_instance().reset()
        nodes = Cache.get_instance().get_nodes()
        for node_id in nodes:
            node = nodes[node_id]
            UDPServer.send('ON', node['addr'], node['port'])

    def alarm_off():
        AlarmManager.get_instance().reset()
        nodes = Cache.get_instance().get_nodes()
        for node_id in nodes:
            node = nodes[node_id]
            UDPServer.send('OFF', node['addr'], node['port'])

    def send_cmd(node_id, cmd):
        node = Cache.get_instance().get_node(node_id)
        if node is None:
            return False
        else:
            UDPServer.send(cmd, node['addr'], node['port'])
        return True

    def keep_alive():
        nodes = Cache.get_instance().get_nodes()
        if len(nodes) == 0:
            return False
        else:
            for node_id in nodes:
                node = nodes[node_id]
                UDPServer.send('STATUS', node['addr'], node['port'])
        return True

    def reset():
        nodes = Cache.get_instance().get_nodes()
        if len(nodes) == 0:
            return False
        else:
            for node_id in nodes:
                node = nodes[node_id]
                UDPServer.send('RESET', node['addr'], node['port'])
        return True

    def status():
        status = dict()
        if AlarmManager.get_instance().get_status():
            status['alarm'] = 'armed'
        else:
            status['alarm'] = 'disarmed'
        status['nodes'] = Cache.get_instance().get_nodes()
        return status
    
    def remove(node_id):
        return Cache.get_instance().remove_node(node_id)