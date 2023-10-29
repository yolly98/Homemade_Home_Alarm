import threading
import json

class Cache:

    instance = None

    def __init__(self):
       self.db_file = 'alarm_status.json'
       self.nodes = dict()
       self.lock = threading.Lock()
       self.laod_status()

    @staticmethod
    def get_instance():
        if Cache.instance is None:
            Cache.instance = Cache()
        return Cache.instance
    
    def get_nodes(self):
        with self.lock:
            nodes = self.nodes.copy()
            return nodes
        
    def get_node(self, node_id):
         with self.lock:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                return node
            else:
                return None

    def save_status(self):
        with open(self.db_file, 'w') as file:
            json.dump(self.nodes, file, indent=4)

    def laod_status(self):
        with open(self.db_file, 'r') as file:
            self.nodes = json.load(file)

    def add_node(self, node_id, node):
        with self.lock:
            self.nodes[node_id] = node
            self.save_status()

    def remove_node(self, node_id):
        with self.lock:
            if node_id in self.nodes:
                self.nodes.pop(node_id, None)
                self.save_status()
                return True
            else:
                return False

