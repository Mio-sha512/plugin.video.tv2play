from .node import Node

class Season(Node):
    def __init__(self, season, plot, thumb):
        self.season = season
        id = season["id"]
        title = season["title"]
        Node.__init__(self, id=id, title=title, plot=plot, thumb=thumb)
