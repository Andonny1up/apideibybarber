from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def delete(self, deleted_by=None, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by
        self.save()