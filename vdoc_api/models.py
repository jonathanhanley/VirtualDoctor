import hashlib

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    code = models.CharField(max_length=5, null=True, default="")


# Create your models here.
class Consultant(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=5, null=True, default="")

    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        super(Consultant, self).save(*args, **kwargs)

    def generate_code(self):
        string = f"{self.user.email} - {self.user.first_name} - {self.user.last_name} - {self.user.username}"
        code = hashlib.sha256(string.encode('utf-8')).hexdigest()
        return code[:5]
