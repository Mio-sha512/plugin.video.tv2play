from resources.lib.api.models.node import Node
from datetime import datetime


class Station(Node):
    def __init__(self, station):
        id = station["guid"]
        title = station["title"]
        thumb = station["presentationArt"]["url"]
        plot =  self.__init_plot(station["epgEntries"]["nodes"])
        Node.__init__(self, title=title, thumb=thumb, plot=plot, id=id)

    def __init_plot(self, entries):
        plot = ""
        for e in entries:
            plot += e["title"]
            start_time = datetime.fromtimestamp(int(e["startUnix"])).strftime("%H:%M")
            end_time = datetime.fromtimestamp(int(e["stopUnix"])).strftime("%H:%M")
            plot += " (%s - %s)\n" % (start_time, end_time)
        return plot

    def get_publication_date(self):
        return ""
