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
from resources.lib.api.models.structure import Structure
from resources.lib.api.models.page import Pages
from resources.lib.api.exception import LoginException



class Router:
    ACTION_SERIE = "serie"
    ACTION_VIDEO = "video"
    ACTION_PLAY = "play"
    ACTION_PAGE = "page"

    def initialize(self, argv):
        G.init_globals(argv) # Has to be executed first!
        if G.FIRST_RUN:
            self.prompt = Prompt()
            self.api = PlayAPI()
            self.pages = Pages()
        G.FIRST_RUN = False
        LOG.info(argv)
        self.params = dict(parse_qsl(argv[2][1:]))
        self.url = argv[0]

    def route(self):
        if self.params:
            action = self.params["action"]
            param = self.params["param"]
            if action == self.ACTION_PAGE:
                self.list_page_content(param)
            elif action == self.ACTION_SERIE:
                self.list_structure_content(param)
            elif action == self.ACTION_VIDEO:
                self.list_videos(param)
            elif action == self.ACTION_PLAY:
                self.play_video(param)
            else:
                raise ValueError("Invalid paramstring: {0}!".format(self.params))
        else:
            self.list_pages()

    def add_directory_item(self, action, node, param=""):
        list_item = xbmcgui.ListItem(label=node.get_title())
        list_item.setInfo("video", {"title": node.get_title(),
                                    "mediatype": "video"})
        thumb = node.get_thumb()
        list_item.setArt({"thumb": thumb,
                          "icon": thumb,
                          "fanart": thumb
                          })
        url = self.get_url(action=action, param=param)
        if node.is_playable():
            list_item.setProperty("IsPlayable", "True")
        xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, node.is_folder())

    def list_pages(self):
        for page in self.pages.pages:
            self.add_directory_item(self.ACTION_PAGE, page, param=page.get_path())
        xbmcplugin.endOfDirectory(G.HANDLE)
    
    def list_page_content(self, page_path):
        LOG.info("Open page: " + page_path)
        for subpage in self.api.get_subpages(page_path):
            self.add_directory_item(self.ACTION_PAGE, subpage, param=subpage.get_path())
        for structure in self.api.get_structures(page_path):
            self.add_directory_item(self.ACTION_SERIE, structure, param=structure.get_id())
        if page_path == "/live":
            for station in self.api.get_stations():
                self.add_directory_item(self.ACTION_PLAY, station, param=station.get_guid())
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

    def list_structure_content(self, structure_id):
        LOG.info("Enter structure: " + structure_id)
        videos, series = self.api.get_structure_content(structure_id)
        for s in series:
            self.add_directory_item(self.ACTION_VIDEO, s, param=s.get_guid())
        for v in videos:
            self.add_directory_item(self.ACTION_PLAY, v, param=v.get_guid())
            xbmcplugin.addSortMethod(G.HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(G.HANDLE)


    def list_videos(self, serie_guid):
        """
        """
        LOG.info("Enter serie: " + serie_guid)
        for v in self.api.get_videos(serie_guid):
            self.add_directory_item(self.ACTION_PLAY, v, param=v.get_guid())
            xbmcplugin.addSortMethod(G.HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(G.HANDLE)

    def play_video(self, video_guid):
        """
        """
        LOG.info("Play video: " + video_guid)
        user = self.api.get_user()
        if user == None:
            username, password = self.prompt.get_credentials()
            try:
                user = self.api.login(username, password)
            except LoginException:
                self.prompt.display_message("Error", "Invalid credentials")
                return
        playback = self.api.get_playback(video_guid, user.client_id, user.access_token)
        if playback == None:
            self.prompt.display_message("Error", "An error occured")
            return 
        player = Player(playback)
        player.play_video()

ROUTER = Router()
