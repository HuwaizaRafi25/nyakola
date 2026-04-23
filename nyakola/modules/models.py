from django.db import models

class Module(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='modul_covers/') # Pastikan folder media sudah di-set
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title