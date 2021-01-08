import sys
try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl
    from urllib import urlencode
import inputstreamhelper
import xbmcgui
import xbmc
import xbmcplugin
from resources.lib.logging import LOG
from resources.lib.globals import G
from resources.lib.view.prompt import Prompt
from resources.lib.view.player import Player
from resources.lib.api.api import PlayAPI
from resources.lib.api.models.category import CATEGORIES

class Router:
    ACTION_SERIE = "serie"
    ACTION_VIDEO = "video"
    ACTION_PLAY = "play"

    def __init__(self, argv):
        G.init_globals(argv) # Has to be executed first!

        self.prompt = Prompt()
        self.api = PlayAPI()
        self.params = dict(parse_qsl(argv[2][1:]))
        self.url = argv[0]

    def route(self):
        if self.params:
            action = self.params["action"]
            if action == self.ACTION_SERIE:
                self.list_series(self.params["category_id"])
            elif action == self.ACTION_VIDEO:
                self.list_videos(self.params["category"])
            elif action == self.ACTION_PLAY:
                self.play_video(self.params["guid"])
            else:
                raise ValueError("Invalid paramstring: {0}!".format(self.params))
        else:
            self.list_categories()
    
    def list_categories(self):
        for category in CATEGORIES:
            list_item = xbmcgui.ListItem(label=category.title)
            list_item.setInfo("video", {"title": category.title,
                                        "genre": category.genre,
                                        "mediatype": "video"})
            url = self.get_url(action=self.ACTION_SERIE, category_id=category.id)
            is_folder = True
            xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, is_folder)
        xbmcplugin.endOfDirectory(G.HANDLE)

    def get_url(self, **kwargs):
        """
        Create a URL for calling the plugin recursively from the given set of keyword arguments.

        :param kwargs: "argument=value" pairs
        :type kwargs: dict
        :return: plugin call URL
        :rtype: str
        """
        return "{0}?{1}".format(self.url, urlencode(kwargs))

    def list_series(self, category_id):
        for s in self.api.get_series(category_id):
            list_item = xbmcgui.ListItem(label=s.title)
            list_item.setInfo("video", {"title": s.title,
                                        "description": s.description,
                                        "thumbnail": s.thumbnail,
                                        "mediatype": "video"})
            url = self.get_url(action=self.ACTION_VIDEO)
            is_folder = True
            xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, is_folder)
        xbmcplugin.endOfDirectory(G.HANDLE)


    def list_videos(self, category):
        """
        """
        xbmcplugin.setPluginCategory(G.HANDLE, category)
        xbmcplugin.setContent(G.HANDLE, "videos")

        list_item = xbmcgui.ListItem(label="Title")
        list_item.setInfo("video", {"title": "Title",
                                    "mediatype": "video"})
        list_item.setProperty("IsPlayable", "true")
        url = self.get_url(action="play", guid="r7-program-234920")
        is_folder = False

        xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, is_folder)
        xbmcplugin.addSortMethod(G.HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(G.HANDLE)

    def play_video(self, guid):
        """
        """
        user = self.api.get_user()
        if user == None:
            username, password = self.prompt.get_credentials()
            user = self.api.login(username, password)
        LOG.info(user.access_token)
        video = self.api.get_video(guid, user.client_id, user.access_token)
        LOG.info(video.license_token)
        player = Player(video)
        player.play_video()






