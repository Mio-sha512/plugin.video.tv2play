class PlayBack:
    def __init__(self, playback):
        self.playback = playback
        self.src = playback["smil"]["video"]["src"]
        self.mime_type = playback["smil"]["video"]["type"]
        self.license_token = playback["smil"]["securityLicense"]["token"]

        url = self.playback["smil"]["securityLicense"]["url"]
        self.license_url = url + "|Content-Type=&User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3041.0 Safari/537.36&Host=lic.drmtoday.com&x-dt-auth-token=%s|R{SSM}|JBlicense" % self.license_token
    
    def __repr__(self):
        return self.playback.__repr__()

