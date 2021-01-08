import requests
from bs4 import BeautifulSoup
from ..logging import LOG
from resources.lib.logging import LOG
from .models.user import User
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

class AuthAPI():
    def __init__(self, cookie_file):
        self.cookie_file = cookie_file
        self.api_url = "https://play.tv2.dk/api/user"

    def login(self, username, password):
        login_url = self.api_url + "/login?return_url=/"
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

        response = sess.get(self.api_url)
        cookies = sess.cookies
        cookies.pop("play.sid") # Remove session id
        self.cookie_file.save(sess.cookies)

        return User(response.json()["user"])

    def get_user(self):
        front_page = "https://play.tv2.dk/forside"
        sess = requests.session()
        cookies = self.cookie_file.load()
        sess.get(front_page, cookies=cookies)
        response = sess.get(self.api_url)
        if response.status_code == 200 and response.json()["user"] != None:
            LOG.log("Got user from from auth cookies")
            return User(response.json()["user"])
        return None
