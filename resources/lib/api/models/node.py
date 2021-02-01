class Node():
    def __init__(self, title="", thumb="", plot="", id=""):
        self.title=title
        self.thumb = thumb
        self.plot = plot
        self.id = id

    def get_title(self):
        return self.title

    def get_id(self):
        return self.id

    def get_thumb(self):
        return self.thumb

    def get_plot(self):
        return self.plot

