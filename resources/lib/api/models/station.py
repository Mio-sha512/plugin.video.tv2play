from resources.lib.api.models.node import Node


class Station(Node):
    def __init__(self, station):
        Node.__init__(self)
        self.id = station["id"]
        self.guid = station["guid"]
        self.title = station["title"]
        self.thumb = station["scalableLogo"]["regular"]
        self.plot = station["description"]

    def get_guid(self):
        return self.guid

    def is_folder(self):
        return False

    def is_playable(self):
        return True
