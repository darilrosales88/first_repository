from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from nomencladores.models import nom_cargo, nom_entidades  # Asegúrate de que los nombres sean correctos

# Modelo de usuario personalizado
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ufc', 'UFC'),
        ('gemar', 'GEMAR'),
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operador',verbose_name="Rol que desempeña")
    entidad = models.ForeignKey(nom_entidades, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Entidad")
    cargo = models.ForeignKey(nom_cargo, on_delete=models.CASCADE, verbose_name="Cargo", blank=True, null=True, )
   

    def create_user(self, username, email, first_name, last_name, password, entidad=None, cargo=None, role="operador", **extra_fields):
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            entidad=entidad,
            cargo=cargo,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"


# Modelo de auditoría
CustomUser = get_user_model()
class Auditoria(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    direccion_ip = models.GenericIPAddressField()
    navegador = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha} - {self.usuario.role}"