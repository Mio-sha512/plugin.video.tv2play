class Video():
    def __init__(self, video):
        self.video = video
        self.episode_number = video["episodeNumber"]
        self.watched = video["watched"]
        self.progress = video["progress"]
        self.guid = video["guid"]
        self.episode_number = video["episodeNumber"]
        self.title = video["originalTitle"]
        if self.episode_number != None:
            self.title = str(self.episode_number) + ". " + self.title
        self.description = video["description"]
        self.thumbnail = video["thumbnail"]["url"]

