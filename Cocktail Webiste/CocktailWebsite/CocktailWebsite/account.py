
class Login:
    login_token = False

    def __init__(self, username, identifier):
        self.username = username
        self.identifier = identifier

    def amend_token(self):
        self.login_token = True


