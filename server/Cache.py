import threading

class Cache:

    instance = None

    def __init__(self):
       self.nodes = dict()
       self.lock = threading.Lock()

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

    def add_node(self, node_id, node):
        with self.lock:
            self.nodes[node_id] = node

    def remove_node(self, node_id):
        with self.lock:
            if node_id in self.nodes:
                self.nodes.pop(node_id, None)
                return True
            else:
                return False

