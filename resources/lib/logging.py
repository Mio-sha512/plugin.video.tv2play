import xbmc

class Logger:
    def __log(self, msg, level):
        xbmc.log("[plugin.video.tv2play] " + msg, level=level)

    def error(self, msg):
        self.__log(msg, xbmc.LOGERROR)

    def info(self, msg):
        self.__log(msg, xbmc.LOGNOTICE)

    def warning(self, msg):
        self.__log(msg, xbmc.LOGWARNING)

LOG = Logger()

