class User:
    def __init__(self, user):
        self.user = None
        self.access_token = user.get("accessToken", None)
        self.client_id = user.get("userId", None)
