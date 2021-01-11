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

class Router:
    ACTION_SERIE = "serie"
    ACTION_VIDEO = "video"
    ACTION_PLAY = "play"
    ACTION_PAGE = "page"

    def __init__(self, argv):
        G.init_globals(argv) # Has to be executed first!

        self.prompt = Prompt()
        self.api = PlayAPI()
        self.params = dict(parse_qsl(argv[2][1:]))
        self.url = argv[0]
        self.pages = Pages()

    def route(self):
        if self.params:
            action = self.params["action"]
            if action == self.ACTION_PAGE:
                self.list_page_content(self.params["page_path"])
            elif action == self.ACTION_SERIE:
                self.list_structure_content(self.params["structure_id"])
            elif action == self.ACTION_VIDEO:
                self.list_videos(self.params["serie_guid"])
            elif action == self.ACTION_PLAY:
                self.play_video(self.params["video_guid"])
            else:
                raise ValueError("Invalid paramstring: {0}!".format(self.params))
        else:
            self.list_pages()

    def list_pages(self):
        for page in self.pages.pages:
            list_item = xbmcgui.ListItem(label=page.title)
            list_item.setInfo("video", {"title": page.title,
                                        "mediatype": "video"})
            url = self.get_url(action=self.ACTION_PAGE, page_path=page.path)
            is_folder = True
            xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, is_folder)
        xbmcplugin.endOfDirectory(G.HANDLE)
    
    def list_page_content(self, page_path):
        LOG.info("Open page: " + page_path)
        for subpage in self.api.get_subpages(page_path):
            list_item = xbmcgui.ListItem(label=subpage.title)
            list_item.setInfo("video", {"title": subpage.title,
                                        "mediatype": "video"})
            url = self.get_url(action=self.ACTION_PAGE, page_path=subpage.path)
            is_folder = True
            xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, is_folder)

        for structure in self.api.get_structures(page_path):
            list_item = xbmcgui.ListItem(label=structure.title)
            list_item.setInfo("video", {"title": structure.title,
                                        "mediatype": "video"})
            url = self.get_url(action=self.ACTION_SERIE, structure_id=structure.id)
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

    def add_directory_item(self, action, title="", plot="", thumb="", is_folder=True, **kwargs):
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo("video", {"title": title,
                                    "plot": plot,
                                    "mediatype": "video"})
        list_item.setArt({"thumb": thumb,
                          "icon": thumb,
                          "fanart": thumb
                          })
        url = self.get_url(action=action, **kwargs)
        xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, is_folder)


    def list_structure_content(self, structure_id):
        LOG.info("Enter structure: " + structure_id)
        videos, series = self.api.get_structure_content(structure_id)
        for s in series:
            self.add_directory_item(
                    self.ACTION_VIDEO,
                    title=s.title,
                    plot=s.description, 
                    thumb=s.thumbnail,
                    is_folder=True,
                    serie_guid=s.guid
                    )
        LOG.info("Videos: " + str(len(videos)))
        for v in videos:
            self.add_directory_item(
                    self.ACTION_PLAY, 
                    title=v.title, 
                    plot=v.description,
                    thumb=v.thumbnail,
                    is_folder=False,
                    video_guid=v.guid 
                )
        xbmcplugin.endOfDirectory(G.HANDLE)


    def list_videos(self, serie_guid):
        """
        """
        LOG.info("Enter serie: " + serie_guid)
        for v in self.api.get_videos(serie_guid):
            list_item = xbmcgui.ListItem(label=v.title)
            list_item.setInfo("video", {"title": v.title,
                                        "plot": v.description,
                                        "mediatype": "video"})
            list_item.setArt({"thumb": v.thumbnail,
                              "icon": v.thumbnail,
                              "fanart": v.thumbnail
                              })
            list_item.setProperty("IsPlayable", "true")
            url = self.get_url(action=self.ACTION_PLAY, video_guid=v.guid)
            is_folder = False

            xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, is_folder)
            xbmcplugin.addSortMethod(G.HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(G.HANDLE)

    def play_video(self, video_guid):
        """
        """
        LOG.info("Play video: " + video_guid)
        user = self.api.get_user()
        if user == None:
            username, password = self.prompt.get_credentials()
            user = self.api.login(username, password)
        video = self.api.get_playback(video_guid, user.client_id, user.access_token)
        player = Player(video)
        player.play_video()






