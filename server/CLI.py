from UDPServer import UDPServer
from AlarmManager import AlarmManager
from Cache import Cache
import os
import signal

class CLI:
    instance = None

    def __init__(self):
       pass

    def init():
        print('--------------------------------------------------')
        print('               HOMEMADE ALARM SERVER              ')
        print('--------------------------------------------------')
        print('insert a command to interact with the system')
        print('COMMANDS:')
        print('- help')
        print('- send [room] [node_id] [cmd]')
        print('- status')
        print('- exit')
        print('- alarm [on/off]')
        print('- keep_alive')
        print('--------------------------------------------------')

    @staticmethod
    def get_instance():
        if CLI.instance is None:
            CLI.instance = CLI()
        return CLI.instance
    
    def listen(self):
        while True:
            cmd = input("> ")
            cmd = cmd.split(' ')
            # menage command
            if cmd[0] == 'help':
                self.init()
            elif cmd[0] == 'status':
                nodes = Cache.get_instance().get_nodes()
                if len(nodes) == 0:
                    print('No sensor nodes connected')
                else:
                    for node_id in nodes:
                        print(nodes[node_id])
            elif cmd[0] == 'exit':
                print('Exit ...')
                try:
                    os.kill(os.getpid(), signal.SIGINT)
                except:
                    pass
            elif cmd[0] == 'alarm':
                if len(cmd) < 2 or (cmd[1] != 'on' and cmd[1] != 'off'):
                    print('wrong command: alarm [on/off]')
                    continue
                AlarmManager.get_instance().reset()
                nodes = Cache.get_instance().get_nodes()
                for node_id in nodes:
                    node = nodes[node_id]
                    if cmd[1] == 'on':
                        UDPServer.send('ON', node['addr'], node['port'])
                    else:
                        UDPServer.send('OFF', node['addr'], node['port'])
            elif cmd[0] == 'send':
                if len(cmd) < 3:
                    print('wrong command: send [room] [node_id] [cmd]')
                    continue
                node_id = f'/{cmd[1]}/{cmd[2]}'
                node = Cache.get_instance().get_node(node_id)
                if node is None:
                    print("Node doesn't exists")
                else:
                    UDPServer.send(cmd[3], node['addr'], node['port'])
            elif cmd[0] == 'keep_alive':
                nodes = Cache.get_instance().get_nodes()
                if len(nodes) == 0:
                    print('No sensor nodes connected')
                else:
                    for node_id in nodes:
                        node = nodes[node_id]
                        UDPServer.send('STATUS', node['addr'], node['port'])


            