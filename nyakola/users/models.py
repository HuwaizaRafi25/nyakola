from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=50, default='siswa')
    foto_profil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    @property
    def role_name(self):
        return self.role.capitalize()

    @property
    def role_color(self):
        # Kamu bisa atur warna hex-nya di sini
        if self.role.lower() == 'admin':
            return '#ffcccc' # Merah muda
        return '#e0f2fe'     # Biru muda

    @property
    def text_color(self):
        if self.role.lower() == 'admin':
            return '#991b1b' # Teks merah gelap
        return '#0369a1'     # Teks biru gelap