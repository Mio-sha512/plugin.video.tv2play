class Video():
    def __init__(self, video):
        self.video = video
        self.episode_number = video["episodeNumber"]
        self.watched = video["watched"]
        self.progress = video["progress"]
        self.guid = video["guid"]
        self.title = video["title"]
        self.description = video["description"]
        self.thumbnail = video["thumbnail"]["url"]

