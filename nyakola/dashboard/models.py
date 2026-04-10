from django.db import models

class UserProfile:
    """
    Representasi struktur data User di MongoDB untuk aplikasi Nyakola.
    Field ini disesuaikan dengan template settings.html kamu.
    """
    def __init__(self, user_id, username, email, fullname, role, phone=None, profile_pic=None, nim=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.fullname = fullname
        self.role = role # 'admin' atau 'student'
        self.phone = phone if phone else "-"
        self.profile_pic = profile_pic
        self.nim = nim # Khusus untuk student