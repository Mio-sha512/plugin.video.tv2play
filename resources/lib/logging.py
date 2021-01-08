import xbmc

class Logger:
    def log(self, msg):
        xbmc.log("plugin.video.tv2play: " + msg, level=xbmc.LOGNOTICE)

    def error(self, msg):
        xbmc.log(msg, xbmc.LOGERROR)

LOG = Logger()

