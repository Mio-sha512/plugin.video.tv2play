import xbmcgui
import xbmc
from resources.lib.globals import G

class Prompt():
    def get_credentials(self):
        dialog = xbmcgui.Dialog()
        username = dialog.input("Enter Email", type=xbmcgui.INPUT_ALPHANUM)
        password = dialog.input("Enter Password", type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
        xbmc.log("Logged in - Email: %s, password: %s" % (username, password), level=xbmc.LOGINFO)
        return (username, password)

    def display_message(self, heading, message):
        dialog = xbmcgui.Dialog()
        dialog.ok(G.ADDON_NAME, message)

    def get_input(self, msg, type=xbmcgui.INPUT_ALPHANUM):
        dialog = xbmcgui.Dialog()
        input = dialog.input(msg, type=type)
        return input




