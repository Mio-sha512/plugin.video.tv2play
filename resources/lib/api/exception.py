class LoginException (Exception):
    pass

class HTTPException(Exception):
    TYPE = "HttpError"

    def __init__(self, title="Http Error", msg="Bad connection, check your internet connection and try again." ):
        self.title = title
        self.msg = msg
        Exception.__init__(self, self.msg)

class ConcurrencyLimitViolationException(Exception):
    TYPE = "ConcurrencyLimitViolation"

    def __init__(self, title="Concurrency Limit Violation", msg="Too many concurrent streams.\nYou might be viewing TV2 play on too many devices"):
        self.title = title
        self.msg = msg
        Exception.__init__(self, self.msg)

class NoTypeException(Exception):
    def __init__(self, title="Error", msg="An unkown error occured.\nView the log for more details."):
        self.title = title
        self.msg = msg
        Exception.__init__(self, self.msg)


