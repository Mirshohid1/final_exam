from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import os


def post_image_path(instance, filename):
    return f"post_images/post_{instance.id}-{filename}"

def user_avatar_path(instance, filename):
    return f"user_avatar/user_{instance.id}-{filename}"

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)


    def delete(self, *args, **kwargs):
        if self.avatar and os.path.isfile(self.avatar.path):
            os.remove(self.avatar.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=post_image_path, blank=True, null=True)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return f"Comment for the post {self.post.title}"

