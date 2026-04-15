from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Field yang sudah ada
    role = models.CharField(max_length=50, default='siswa')
    foto_profil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # --- TAMBAHAN BARU ---
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # ---------------------

    @property
    def role_name(self):
        return self.role.capitalize()

    @property
    def role_color(self):
        if self.role.lower() == 'admin':
            return '#ffcccc' 
        return '#e0f2fe'     

    @property
    def text_color(self):
        if self.role.lower() == 'admin':
            return '#991b1b' 
        return '#0369a1'