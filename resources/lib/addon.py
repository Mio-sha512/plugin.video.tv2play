# -*- coding: utf-8 -*-

import sys
import xbmcaddon
import xbmcgui
import xbmc
from .routing import Router
from .user import User
from .api import PlayAPI

class Addon:
    def __init__(self):
        ADDON = xbmcaddon.Addon()
        self.addonname = ADDON.getAddonInfo("name")
        self.user = User()
        self.api = PlayAPI()

    def run(self):
        router = Router(self.api, User())
        router.route()

