import xbmcvfs
import pickle
import xbmc
import os

from resources.lib.logging import LOG
from resources.lib.globals import G

class CookieFile():
    def __init__(self, path, file_name):
        self.path = path
        self.file_name = file_name
        self.file_path = os.path.join(path, file_name)

    def save(self,cookie_jar):
        """Save a cookie jar to file and in-memory storage"""
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(self.file_path, "wb") as cookie_file:
            cookie_file.write(bytearray(pickle.dumps(cookie_jar)))

    def delete(self):
        """Delete cookies for an account from the disk"""
        os.remove(self.file_path)

    def load(self):
        """Load cookies for a given account"""
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, "rb") as cookie_file:
            cookie_file = xbmcvfs.File(self.file_path, 'rb')
            cookie_jar = pickle.loads(cookie_file.readBytes())
        return cookie_jar
