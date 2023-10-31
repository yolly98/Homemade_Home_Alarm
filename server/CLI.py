from UDPServer import UDPServer
from AlarmManager import AlarmManager
from Cache import Cache
from Protocols import Protocols
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
        print('- send [room] [id] [cmd]')
        print('- remove [room] [id]')
        print('- status')
        print('- exit')
        print('- alarm [on/off]')
        print('- keep_alive')
        print('- reset')
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

            # ----- HELP COMMAND ----- #
            if cmd[0] == 'help':
                CLI.init()
            elif cmd[0] == 'status':
                status = Protocols.status()
                print('----------------------------------')
                print(f"alarm: {status['alarm']}")
                print(f"alerted: {status['alerted']}")
                if len(status['nodes']) == 0:
                    print('No sensor nodes connected')
                else:
                    for node_id in status['nodes']:
                        print(status['nodes'][node_id])
                print('----------------------------------')

            # ----- EXIT COMMAND ----- #
            elif cmd[0] == 'exit':
                print('Exit ...')
                try:
                    os.kill(os.getpid(), signal.SIGINT)
                except:
                    pass
            
            # ----- ALRM ON/OFF COMMAND ----- #
            elif cmd[0] == 'alarm':
                if len(cmd) < 2 or (cmd[1] != 'on' and cmd[1] != 'off'):
                    print('wrong command: alarm [on/off]')
                    continue
                if cmd[1] == 'on':
                    Protocols.alarm_on()
                else:
                    Protocols.alarm_off()

            # ----- SEND COMMAND ----- #
            elif cmd[0] == 'send':
                if len(cmd) < 4:
                    print('wrong command: send [room] [id] [cmd]')
                    continue
                node_id = f'/{cmd[1]}/{cmd[2]}'
                res = Protocols.send_cmd(node_id, cmd[3])
                if not res:
                    print("Node doesn't exists")
            
            # ----- KEEP_ALIVE COMMAND ----- #
            elif cmd[0] == 'keep_alive':
                res = Protocols.keep_alive()
                if not res:
                    print('No sensor nodes connected')

            # ----- RESET COMMAND ----- #
            elif cmd[0] == 'reset':
                res = Protocols.reset()
                if not res:
                    print('No sensor nodes connected')

            # ----- REMOVE NODE ---- #
            elif cmd[0] == 'remove':
                if len(cmd) < 3:
                    print('wrong command: remove [room] [id]')
                    continue
                node_id = f'/{cmd[1]}/{cmd[2]}'
                res = Protocols.remove(node_id)
                if not res:
                    print("Node doesn't exists")


            