import hashlib

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


# Create your models here.
class Consultant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, null=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.code = self.generate_code()

    def generate_code(self):
        string = f"{self.user.email} - {self.user.first_name} - {self.user.last_name} - {self.user.username}"
        code = hashlib.sha256(string.encode('utf-8')).hexdigest()
        return code[:5]