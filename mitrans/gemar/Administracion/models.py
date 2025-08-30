from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('GEMAR', 'Usuario GEMAR'),
    ]
    
    rol = models.CharField(
        max_length=10,
        choices=ROL_CHOICES,
        default='GEMAR'
    )
    
    def is_gemar_user(self):
        return self.rol == 'GEMAR' or self.is_superuser
    
    def is_admin_user(self):
        return self.is_superuser