from .node import Node
from datetime import datetime

class Video(Node):
    def __init__(self, video):
        id = video["guid"]
        plot = video["description"]
        thumb = video["thumbnail"]["url"]
        title = video.get("title", None)
        Node.__init__(self, title=title, plot=plot, thumb=thumb, id=id)

        self.video = video
        episode_number = video.get("episodeNumber", None)
        self.episode_number = "0" + str(episode_number) if episode_number < 10 else str(episode_number)
        season_number = video.get("seasonNumber", None)
        self.season_number = "0" + str(season_number) if season_number < 10 else str(season_number)

        self.publication_date = None
        if video.get("firstPublicationDate", None) != None:
            self.publication_date = datetime.fromtimestamp(int(video.get("firstPublicationDate", None)) / 1000).strftime("%d.%m.%Y")
        self.watched = video.get("watched", None)
        if self.episode_number != None and self.season_number != None:
            self.title = "%sx%s - %s" % ( self.season_number, self.episode_number, self.title )

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
