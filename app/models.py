from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Domain(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    details=models.JSONField(null=True)
    ports=models.JSONField(null=True)
    subdomains=models.JSONField(null=True)

    def __str__(self):
        return self.user