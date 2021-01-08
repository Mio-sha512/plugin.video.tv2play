class Category():
    def __init__(self):
        self.title = None
        self.id = None
        self.genre = None

class ComedyCategory(Category):
    def __init__(self):
        self.title = "Comedy"
        self.id = "U3RydWN0dXJlOnVybMKke2NvbnRlbnR9L3Byb2dyYW1zL3Nlcmllcz9jYXRlZ29yeT1Db21lZHl8dGl0bGXCpENvbWVkeXxwcmVzZW50YXRpb27CpGZpbHRlcnBhbmVsfHBsYXRmb3JtwqR1bmRlZmluZWR8b3B0aW9uwqR1bmRlZmluZWQ="
        self.genre = "Comedy"


CATEGORIES = [
        ComedyCategory(),
    ]


