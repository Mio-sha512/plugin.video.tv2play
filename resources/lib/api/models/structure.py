from .node import Node

class Structure(Node):
    def __init__(self, structure):
        title = structure["title"]
        id = structure["id"]
        Node.__init__(self, title=title, id=id)


