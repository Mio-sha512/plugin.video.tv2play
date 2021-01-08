import requests
from resources.lib.api.models.video import Video
from resources.lib.api.auth import AuthAPI
from resources.lib.api.cookies import CookieFile
from resources.lib.api.graphql import GraphQL_API
from resources.lib.globals import G

class PlayAPI:
    def __init__(self):
        self.auth = AuthAPI(CookieFile(G.DATA_PATH, G.COOKIES_FILE_NAME))
        self.graphql = GraphQL_API()

    def get_user(self):
        return self.auth.get_user()

    def login(self, username, password):
        return self.auth.login(username, password)

    def get_video(self, guid, client_id, access_token):
        return self.graphql.get_video(guid, client_id, access_token)
    
    def get_series(self, category):
        return self.graphql.get_series(category)
