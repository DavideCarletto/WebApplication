from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, psd, username, type):
        self.id = id
        self.email = email
        self.psd = psd
        self.username = username
        self.type = type