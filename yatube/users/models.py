from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='user.png', upload_to='profile_pics/', blank=True, null=True)
    tg = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
