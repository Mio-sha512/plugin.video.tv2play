import sys
from urllib import urlencode
from urlparse import parse_qsl
import inputstreamhelper
import xbmcgui
import xbmc
import xbmcplugin
from .logger import Logger

class Router:
    def __init__(self, api, user):
        self.params = dict(parse_qsl(sys.argv[2][1:]))
        self.url = sys.argv[0]
        self.handle = int(sys.argv[1])
        self.api = api
        self.user = user
        self.logger = Logger()

    def route(self):
        param_string = sys.argv[2][1:]
        params = dict(parse_qsl(param_string))
        if params:
            if params['action'] == 'listing':
                pass
                self.list_videos(params['category'])
            elif params['action'] == 'play':
                self.play_video(params['guid'])
            else:
                raise ValueError('Invalid paramstring: {0}!'.format(param_string))
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
        xbmcplugin.addDirectoryItem(self.handle, url, list_item, is_folder)
        xbmcplugin.endOfDirectory(self.handle)

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
        Create the list of playable videos in the Kodi interface.

        :param category: Category name
        :type category: str
        """
        xbmcplugin.setPluginCategory(self.handle, category)
        xbmcplugin.setContent(self.handle, 'videos')

        list_item = xbmcgui.ListItem(label="Title")
        list_item.setInfo('video', {'title': "Title",
                                    'mediatype': 'video'})
        list_item.setProperty('IsPlayable', 'true')
        url = self.get_url(action='play', guid="r7-program-234920")
        is_folder = False

        xbmcplugin.addDirectoryItem(self.handle, url, list_item, is_folder)
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(self.handle)

    def play_video(self, guid):
        """
        Play a video by the provided path.

        :param path: Fully-qualified video URL
        :type path: str
        """
        self.user.login()
        access_token =  self.user.get_access_token()
        client_id = self.user.get_client_id()
        video = self.api.get_video(guid, client_id, access_token)
        self.logger.log(video.__repr__())
        license_token = video["playback"]["smil"]["securityLicense"]["token"]
        url_licence_key = video["playback"]["smil"]["securityLicense"]["url"] + "|Content-Type=&User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3041.0 Safari/537.36&Host=lic.drmtoday.com&x-dt-auth-token=%s|R{SSM}|JBlicense" % license_token
        src = video["playback"]["smil"]["video"]["src"]
        mime_type = video["playback"]["smil"]["video"]["type"]
        list_item = xbmcgui.ListItem(path=src)
        list_item.setContentLookup(False)
        list_item.setMimeType(mime_type)
        is_helper = inputstreamhelper.Helper('mpd', drm='widevine')
        inputstream_ready = is_helper.check_inputstream()
        if not inputstream_ready:
            return
        KODI_VERSION_MAJOR = int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])
        if KODI_VERSION_MAJOR >= 19:
            list_item.setProperty('inputstream', is_helper.inputstream_addon)
        else:
            list_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
        list_item.setProperty(
            key=is_helper.inputstream_addon + '.license_type',
            value='com.widevine.alpha')
        list_item.setProperty(
            key=is_helper.inputstream_addon + '.manifest_type',
            value='mpd')
        list_item.setProperty(
            key=is_helper.inputstream_addon + '.license_key',
            value= url_licence_key)
        list_item.setProperty(
            key='inputstream',
            value=is_helper.inputstream_addon)
        xbmcplugin.setResolvedUrl(self.handle, True, listitem=list_item)















