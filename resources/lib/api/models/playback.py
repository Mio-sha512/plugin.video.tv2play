class PlayBack:
    def __init__(self, playback):
        self.playback = playback
        self.src = playback["smil"]["video"]["src"]
        self.mime_type = playback["smil"]["video"]["type"]
        self.license_token = playback["smil"]["securityLicense"]["token"]

        url = self.playback["smil"]["securityLicense"]["url"]
        # self.license_url = url + "|Content-Type=&User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3041.0 Safari/537.36&Host=lic.drmtoday.com&x-dt-auth-token=%s|R{SSM}|JBlicense" % self.license_token

        self.license_url = url
        self.license_url += "|Content-Type="
        self.license_url += "&Accept=*/*"
        self.license_url += "&Accept-Encoding=gzip, deflate, br"
        self.license_url += "&Accept-Language=en-US,en;q=0.9,da;q=0.8"
        self.license_url += "&User-Agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        self.license_url += "&sec-ch-ua=\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\""
        self.license_url += "&sec-ch-ua-mobile=?0"
        self.license_url += "&sec-ch-ua-platform=\"Linux\""
        self.license_url += "&Host=lic.drmtoday.com"
        self.license_url += "&x-dt-auth-token=%s|R{SSM}|JBlicense" % self.license_token
    
    def __repr__(self):
        return self.playback.__repr__()

