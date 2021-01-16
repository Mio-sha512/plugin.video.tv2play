from .node import Node

class Serie(Node):
    def __init__(self, serie):
        Node.__init__(self)
        self.serie = serie
        self.id = serie["id"]
        self.guid = serie["guid"]
        self.title = serie["title"]
        self.plot = serie["description"]
        self.thumb = serie["thumbnail"]["url"]

    def get_guid(self):
        return self.guid

    def is_folder(self):
        return True

    def is_playable(self):
        return False
