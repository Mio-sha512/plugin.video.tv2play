class User:
    def __init__(self, user):
        self.user = user
        self.access_token = user.get("accessToken", None)
        self.access_token = user.get("userId", None)
