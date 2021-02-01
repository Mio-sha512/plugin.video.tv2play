from .node import Node

class Video(Node):
    def __init__(self, video):
        id = video["guid"]
        plot = video["description"]
        thumb = video["thumbnail"]["url"]
        title = video.get("title", None)
        Node.__init__(self, title=title, plot=plot, thumb=thumb, id=id)

        self.video = video
        self.episode_number = video.get("episodeNumber", None)
        self.season_number = video.get("seasonNumber", None)
        self.publication_date = video.get("firstPublicationDate", None)
        self.watched = video.get("watched", None)
        self.progress = video.get("progress", None)
        if self.episode_number != None and self.season_number != None:
            self.title = "S%d/E%d - %s" % ( self.season_number, self.episode_number, self.title )

    def get_publication_date(self):
        return self.publication_date
