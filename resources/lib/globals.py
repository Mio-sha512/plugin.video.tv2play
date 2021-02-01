import os
import xbmcaddon
import xbmc

class Globals():
    def __init__(self):
        self.ADDON = None
        self.ADDON_NAME = None
        self.DATA_PATH = None
        self.HANDLE = None
        self.COOKIES_FILE_NAME = None
        self.FIRST_RUN = True

    def init_globals(self, argv):
        if self.FIRST_RUN:
            self.ADDON = xbmcaddon.Addon()
            self.ADDON_NAME = self.ADDON.getAddonInfo("name")
            self.DATA_PATH = xbmc.translatePath(self.ADDON.getAddonInfo('profile'))
            self.COOKIES_FILE_NAME = xbmc.translatePath(os.path.join(self.DATA_PATH, 'COOKIES'))
            self.HANDLE = int(argv[1])

G = Globals()
