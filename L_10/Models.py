from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, psd, profile_img_path):
        self.id = id
        self.username = username
        self.psd = psd
        self.profile_img_path = profile_img_path
