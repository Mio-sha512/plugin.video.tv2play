from resources.lib.globals import G
import xbmcgui
import xbmcplugin
import xbmc
import inputstreamhelper
from resources.lib.logging import LOG

class Player():
    def __init__(self, video):
        self.video = video

    def play_video(self):
        LOG.info("Playing video at: " + self.video.src)
        list_item = xbmcgui.ListItem(path=self.video.src)
        list_item.setContentLookup(False)
        list_item.setMimeType(self.video.mime_type)

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
                key=is_helper.inputstream_addon + ".manifet_update_parameter",
                value="full")

        list_item.setProperty(
            key=is_helper.inputstream_addon + '.license_key',
            value=self.video.license_url)

        list_item.setProperty(
            key='inputstream',
            value=is_helper.inputstream_addon)
        xbmcplugin.setResolvedUrl(G.HANDLE, True, listitem=list_item)

