import requests

class PlayAPI:
    def __init__(self):
        self.api_url = "https://api.ovp.tv2.dk"

    def __get_headers(self, access_token):
        headers = {
                "Authorization": access_token
        }
        return headers

    def get_video(self, guid, client_id, access_token):
        query = """query  {
          playback(
            guid: "%s"
            format: ["application/dash+xml"]
            platform: play_web
          ) {
            subtitles {
              useAsDefault
            }
            progress {
              position
            }
            pid
            smil(clientId: "%s") {
              video {
                src
                type
              }
              securityLicense {
                url
                token
              }
            }
          }
        }""" % ( guid, client_id )
        headers = self.__get_headers(access_token)
        response = requests.post(self.api_url, json={"query": query }, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        return None

