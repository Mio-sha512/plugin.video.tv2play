from .node import Node

class Video(Node):
    def __init__(self, video):
        Node.__init__(self)
        self.video = video
        self.episode_number = video.get("episodeNumber", None)
        self.season_number = video.get("seasonNumber", None)
        self.watched = video.get("watched", None)
        self.progress = video.get("progress", None)
        self.guid = video["guid"]
        self.title = video.get("title", None)
        if self.episode_number != None and self.season_number != None:
            self.title = "S%d/E%d - %s" % ( self.season_number, self.episode_number, self.title )
        self.plog = video["description"]
        self.thumb = video["thumbnail"]["url"]

    def get_guid(self):
        return self.guid

    def is_folder(self):
        return False

    def is_playable(self):
        return True
