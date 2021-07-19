from .node import Node

class Serie(Node):
    def __init__(self, serie):
        serie = serie
        id = serie["guid"]
        title = serie["title"]
        plot = serie["description"]
        thumb = None
        thumbnail = serie.get("thumbnail", None)
        if thumbnail != None:
            thumb = thumbnail.get("url", None)
        Node.__init__(self, id=id, title=title, plot=plot, thumb=thumb)
