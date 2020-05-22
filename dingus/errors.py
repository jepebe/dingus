class ParserError(Exception):
    def __init__(self, token, message):
        super(ParserError, self).__init__(message)
        self.token = token
        self.message = message
