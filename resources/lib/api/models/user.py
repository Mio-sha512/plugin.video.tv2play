import uuid

class User:
    def __init__(self, user):
        self.user = None
        self.access_token = user.get("accessToken", None)
        self.client_id = user.get("userId", None)
        self.device_id = str( uuid.uuid4() )
