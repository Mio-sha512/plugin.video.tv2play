class Video:
    def __init__(self, video):
        self.video = video
        self.src = video["playback"]["smil"]["video"]["src"]
        self.mime_type = video["playback"]["smil"]["video"]["type"]
        self.license_token = video["playback"]["smil"]["securityLicense"]["token"]

        url = self.video["playback"]["smil"]["securityLicense"]["url"]
        self.license_url = url + "|Content-Type=&User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3041.0 Safari/537.36&Host=lic.drmtoday.com&x-dt-auth-token=%s|R{SSM}|JBlicense" % self.license_token
    
    def __repr__(self):
        return self.video.__repr__()

