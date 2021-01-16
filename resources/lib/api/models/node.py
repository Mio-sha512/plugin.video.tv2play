class Node():
    def __init__(self):
        self.title = ""
        self.thumb = ""
        self.plot = ""

    def get_title(self):
        return self.title

    def get_thumb(self):
        return self.thumb

    def get_plot(self):
        return self.plot

    def is_folder(self):
        raise NotImplementedError
    
    def is_playable(self):
        raise NotImplementedError



