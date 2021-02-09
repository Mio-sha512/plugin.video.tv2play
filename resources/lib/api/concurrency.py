import requests
from resources.lib.logging import LOG
from xbmc import Player
import time

class ConcurrencyLock:
    def __init__(self, meta=None):
        self.url = "https://concurrency.delivery.theplatform.eu/concurrency/web/Concurrency/?schema=1.0&form=json"
        if meta == None:
            self.meta = None
            self.encrypted_lock = None
            self.lock_id = None
            self.sequence_token = None
        else:
            self.set_meta(meta)

    def set_meta(self, meta):
        self.meta = meta
        self.lock_id = meta[3]["content"]
        self.sequence_token = meta[4]["content"]
        self.encrypted_lock = meta[5]["content"]

    def is_locked(self):
        return self.meta != None

    def unlock(self, client_id, session):
        if self.meta != None:
            data = {
                    "unlock": { 
                        "clientId": client_id, 
                        "encryptedLock": self.encrypted_lock,
                        "id": self.lock_id,
                        "sequenceToken": self.sequence_token
                }
            }
            response = requests.post(self.url, json=data)
            return response.status_code
        return 0


    
