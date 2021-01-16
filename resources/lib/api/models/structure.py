from .node import Node

class Structure(Node):
    def __init__(self, structure):
        Node.__init__(self)
        self.title = structure["title"]
        self.id = structure["id"]

    def get_id(self):
        return self.id
    
    def is_folder(self):
        return True

    def is_playable(self):
        return False



