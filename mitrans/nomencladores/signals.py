from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

@receiver(post_migrate)
def rename_default_permissions(sender, **kwargs):
    # Verificar si el sender es una aplicación con modelos
    if not hasattr(sender, 'get_models'):
        return

    # Obtener todos los modelos de la aplicación
    for model in sender.get_models():
        content_type = ContentType.objects.get_for_model(model)

        # Definir los nuevos nombres de los permisos
        new_permissions = {
            'add': _('Insertar'),
            'change': _('Editar'),
            'delete': _('Eliminar'),
            'view': _('Visualizar'),
        }

        # Recorrer los permisos y actualizar sus nombres
        for codename, new_name in new_permissions.items():
            try:
                permission = Permission.objects.get(
                    content_type=content_type,
                    codename=f'{codename}_{model._meta.model_name}'
                )
                permission.name = f'{new_name} {model._meta.verbose_name}'
                permission.save()
            except Permission.DoesNotExist:
                pass