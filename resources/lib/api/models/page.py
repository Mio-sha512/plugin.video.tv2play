from .node import Node

class Page(Node):
    def __init__(self, page):
        Node.__init__(self)
        self.title = page["title"]
        self.path = page["path"]

    def get_path(self):
        return self.path

    def is_folder(self):
        return True

    def is_playable(self):
        return False

class Pages():
    PAGES = [
        { 
            "title" : "Forside",
            "path": "/"
        },
        { 
            "title" : "Live TV",
            "path": "/live"
        },
        { 
            "title" : "Udforsk",
            "path": "/udforsk"
        },
        { 
            "title" : "Nyheder",
            "path": "/nyheder"
        },
        { 
            "title" : "Sport",
            "path": "/sport"
        },
        { 
            "title" : "Boern",
            "path": "/boern"
        },
    ]
    def __init__(self):
        self.pages = []
        for p in self.PAGES:
            self.pages.append(Page(p))



