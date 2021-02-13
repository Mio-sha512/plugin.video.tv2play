from resources.lib.api.models.node import Node


class Station(Node):
    def __init__(self, station):
        id = station["guid"]
        title = station["title"]
        thumb = station["presentationArt"]["url"]
        plot = station["description"]
        Node.__init__(self, title=title, thumb=thumb, plot=plot, id=id)

    def get_publication_date(self):
        return ""
