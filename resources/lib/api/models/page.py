class Page():
    def __init__(self, page):
        self.title = page["title"]
        self.path = page["path"]


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



