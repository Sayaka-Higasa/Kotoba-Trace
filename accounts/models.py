from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import User

class PasswordReset(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    password_token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)

    password_expiry = models.DateTimeField()

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
