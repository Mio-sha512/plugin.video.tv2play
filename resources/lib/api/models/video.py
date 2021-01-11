class Video():
    def __init__(self, video):
        self.video = video
        self.episode_number = video.get("episodeNumber", None)
        self.watched = video.get("watched", None)
        self.progress = video.get("progress", None)
        self.guid = video["guid"]
        self.title = video.get("title", None)
        if self.episode_number != None:
            self.title = str(self.episode_number) + ". " + self.title
        self.description = video["description"]
        self.thumbnail = video["thumbnail"]["url"]

