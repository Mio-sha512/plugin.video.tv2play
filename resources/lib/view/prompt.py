import xbmcgui
import xbmc

class Prompt():
    def get_credentials(self):
        dialog = xbmcgui.Dialog()
        username = dialog.input("Enter Email", type=xbmcgui.INPUT_ALPHANUM)
        password = dialog.input("Enter Password", type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
        xbmc.log("Logged in - Email: %s, password: %s" % (username, password), level=xbmc.LOGINFO)
        return (username, password)


