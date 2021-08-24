from .node import Node
from datetime import datetime

class Video(Node):
    def __init__(self, video):
        id = video["guid"]
        plot = video["description"] 
        if video.get("firstPublicationDate", None) != None:
            self.publication_date = datetime.fromtimestamp(int(video.get("firstPublicationDate", None)) / 1000).strftime("%d.%m.%Y")
            plot = "Sendt %s\n%s" % (plot, self.publication_date)
        thumb = None
        if video.get("thumbnail", None) != None:
            thumb = video["thumbnail"]["url"]
        title = video.get("title", None)
        Node.__init__(self, title=title, plot=plot, thumb=thumb, id=id)

        self.video = video
        self.episode_number = None
        self.season_number = None

        self.publication_date = None
        if video.get("firstPublicationDate", None) != None:
            self.publication_date = datetime.fromtimestamp(int(video.get("firstPublicationDate", None)) / 1000).strftime("%d.%m.%Y")
        self.watched = video.get("watched", None)
        if video.get("episodeNumber", None) != None:
            episode_number = video["episodeNumber"]
            self.title = "%d. %s" % ( episode_number, self.title )

    def get_publication_date(self):
        return self.publication_date

    def get_episode(self):
        return self.episode_number

    def get_season(self):
        return self.season_number

    def get_progress(self):
        if self.video.get("progress", None):
            return (self.video["progress"]["position"], self.video["progress"]["duration"])

    def in_progress(self):
        return self.video.get("progress", None)

    def get_playcount(self):
        if self.watched:
            return 1
        return 0
