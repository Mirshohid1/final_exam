from django.db import models
from django.contrib.auth.models import AbstractUser

def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.id}/{filename}"

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    def delete(self, *args, **kwargs):
        if self.avatar:
            self.avatar.delete()
        super().delete(*args, **kwargs)