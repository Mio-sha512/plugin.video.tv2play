import xbmcgui
import xbmc
import requests
from bs4 import BeautifulSoup
from .logger import Logger
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

class User:
    def __init__(self):
        self.user = None
        self.logger = Logger()
    
    def login(self):
        dialog = xbmcgui.Dialog()
        username = dialog.input("Enter Email", type=xbmcgui.INPUT_ALPHANUM)
        password = dialog.input("Enter Password", type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
        xbmc.log("Logged in - Email: %s, password: %s" % (username, password), level=xbmc.LOGNOTICE)

        login_url = "https://play.tv2.dk/api/user/login?return_url=/"
        sess = requests.session()
        response = sess.get(login_url)

        url_params = parse_qs(urlparse(response.url).query)

        url = "https://auth.tv2.dk/usernamepassword/login"
        data = {
                "username": username,
                "password": password,
                "connection": "TV-2-AWS-Login",
                "state" : url_params["state"][0],
                "client_id" : url_params["client"][0],
                "scope": url_params["scope"][0],
                "tenant": "tv2dk-prod"
            }

        response = sess.post(url, data=data)

        soup = BeautifulSoup(response.text, "html.parser")
        data = {}
        for i in soup.find_all("input"):
            data[i.get("name")] = i.get("value")
        url = soup.form.get("action")
        response = sess.post(url, data=data)

        response = sess.get("https://play.tv2.dk/api/user")
        self.user = response.json()["user"]
        self.logger.log(self.user.__repr__())


    def get_access_token(self):
        return self.user.get("accessToken", None)
    
    def get_client_id(self):
        return self.user.get("userId")

