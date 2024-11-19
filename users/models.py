from django.db import models
from django.contrib.auth.models import AbstractUser

import os


def user_avatar_path(instance, filename):
    return f"user_avatar/user_{instance.username}-{filename}"

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    subscriptions = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="subscribers",
        blank=True,
    )

    def delete(self, *args, **kwargs):
        if self.avatar and os.path.isfile(self.avatar.path):
            os.remove(self.avatar.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username

class FollowedUserNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followed_user_notifications')
    followed_user = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"followed {self.followed_user} to {self.user.username}. is read ? {self.is_read}"

class CommentPostNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_post_notifications')
    comment_post = models.IntegerField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"A comment has been sent to this post_id: {self.comment_post}. is read ? {self.is_read}"