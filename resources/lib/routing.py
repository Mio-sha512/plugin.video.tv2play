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
from .logging import LOG
from .globals import G
from .view.prompt import Prompt
from .view.player import Player
from .api.api import PlayAPI

class Router:
    def __init__(self, argv):
        G.init_globals(argv) # Has to be executed first!

        self.params = dict(parse_qsl(argv[2][1:]))
        self.url = argv[0]
        self.prompt = Prompt()
        self.api = PlayAPI()

    def route(self):
        if self.params:
            if self.params['action'] == 'listing':
                pass
                self.list_videos(self.params['category'])
            elif self.params['action'] == 'play':
                self.play_video(self.params['guid'])
            else:
                raise ValueError('Invalid paramstring: {0}!'.format(self.params))
        else:
            self.list_categories()
    
    def list_categories(self):
        category = "category"
        list_item = xbmcgui.ListItem(label=category)
        list_item.setInfo('video', {'title': "title",
                                    'genre': "gener",
                                    'mediatype': 'video'})
        url = self.get_url(action='listing', category=category)
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
        return '{0}?{1}'.format(self.url, urlencode(kwargs))

    def list_videos(self, category):
        """
        """
        xbmcplugin.setPluginCategory(G.HANDLE, category)
        xbmcplugin.setContent(G.HANDLE, 'videos')

        list_item = xbmcgui.ListItem(label="Title")
        list_item.setInfo('video', {'title': "Title",
                                    'mediatype': 'video'})
        list_item.setProperty('IsPlayable', 'true')
        url = self.get_url(action='play', guid="r7-program-234920")
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
        LOG.log(user.access_token)
        video = self.api.get_video(guid, user.client_id, user.access_token)
        LOG.log(video.license_token)
        player = Player(video)
        player.play_video()






