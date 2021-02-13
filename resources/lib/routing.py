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
from resources.lib.api.exception import ConcurrencyLimitViolationException, HTTPException


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

    def login(self):
        try:
            is_authenticated = self.api.is_authenticated()
            if is_authenticated:
                LOG.info("Already authenticated")
                return True
            if not self.api.login_with_cookie():
                username, password = self.prompt.get_credentials()
                if not self.api.login(username, password):
                    self.prompt.display_message("Error", "Invalid credentials")
                    return False
                else:
                    return True
            return True
        except HTTPException as exp:
            self.prompt.display_message(exp.title, exp.msg)
            return False

    def route(self):
        if not self.login():
            return
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

    def add_list_item(self, action, label="", info={}, art={}, param="", is_folder=True):
        list_item = xbmcgui.ListItem(label=label)
        list_item.setInfo("video", info)
        list_item.setArt(art)
        url = self.get_url(action=action, param=param)
        if not is_folder:
            list_item.setProperty("IsPlayable", "True")
        xbmcplugin.addDirectoryItem(G.HANDLE, url, list_item, is_folder)


    def add_directory(self, action, node, param=""):
        label = node.get_title()
        info = {"title": node.get_title(),
                "mediatype": "video",
                "plot": node.get_plot()}
        thumb = node.get_thumb()
        art = {"thumb": thumb,
                "icon": thumb,
                "fanart": thumb
            }
        self.add_list_item(action, label=label, info=info, art=art,param=param)

    def add_video(self, action, video, param=""):
        label = video.get_title()
        LOG.info("WATCHED: " + str(video.get_playcount()))
        info = {"title": video.get_title(),
                "mediatype": "video",
                "plot": video.get_plot(),
                "date": video.get_publication_date(),
                "episode": video.get_episode(),
                "season": video.get_season(),
                "playcount": video.get_playcount()
            }

        if video.in_progress():
            position, duration = video.get_progress()
            info["position"] = position
            info["duration"] = duration

        thumb = video.get_thumb()
        art = { "thumb": thumb,
                "icon": thumb,
                "fanart": thumb
            }
        self.add_list_item(action,label=label, info=info, art=art, param=param, is_folder=False)

    def add_station(self, action, station, param=""):
        label = station.get_title()
        info = {"title": station.get_title(),
                "mediatype": "video",
                "plot": station.get_plot(),
            }
        thumb = station.get_thumb()
        art = { "thumb": thumb,
                "icon": thumb,
                "fanart": thumb
            }
        self.add_list_item(action,label=label, info=info, art=art, param=param, is_folder=False)

    def list_pages(self):
        for page in self.pages.pages:
            self.add_directory(self.ACTION_PAGE, page, param=page.get_id())
        xbmcplugin.endOfDirectory(G.HANDLE)
    
    def list_page_content(self, page_id):
        LOG.info("Open page: " + page_id)
        for subpage in self.api.get_subpages(page_id):
            self.add_directory(self.ACTION_PAGE, subpage, param=subpage.get_id())
        for structure in self.api.get_structures(page_id):
            self.add_directory(self.ACTION_SERIE, structure, param=structure.get_id())
        if page_id == "/live":
            for station in self.api.get_stations():
                self.add_station(self.ACTION_PLAY, station, param=station.get_id())
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
            self.add_directory(self.ACTION_VIDEO, s, param=s.get_id())
        for v in videos:
            self.add_video(self.ACTION_PLAY, v, param=v.get_id())
            xbmcplugin.addSortMethod(G.HANDLE, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.endOfDirectory(G.HANDLE)


    def list_videos(self, serie_guid):
        """
        """
        LOG.info("Enter serie: " + serie_guid)
        for v in self.api.get_videos(serie_guid):
            self.add_video(self.ACTION_PLAY, v, param=v.get_id())
            xbmcplugin.addSortMethod(G.HANDLE, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.endOfDirectory(G.HANDLE)

    def play_video(self, video_guid):
        """
        """
        LOG.info("Play video: " + video_guid)
        try:
            playback = self.api.get_playback(video_guid)
        except ConcurrencyLimitViolationException as exp:
            self.prompt.display_message(exp.title, exp.msg)
        except HTTPException as exp:
            self.prompt.display_message(exp.title, exp.msg)
        else:
            if playback == None:
                self.prompt.display_message("Error", "An error occured")
                return 
            player = Player(playback)
            player.play_video()

ROUTER = Router()
