from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

def user_upload_path(instance, filename):
    return f"profiles/{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=user_upload_path, null=True, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # any other profile fields

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    text = models.CharField(max_length=300)
    url = models.CharField(max_length=300, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notif for {self.user.username}: {self.text[:40]}"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    action = models.CharField(max_length=200)
    meta = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.action} @ {self.created_at}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
