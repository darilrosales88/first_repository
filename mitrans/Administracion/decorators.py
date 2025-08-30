from functools import wraps
from .models import Auditoria

def audit_log(action_verb):
    """
    Decorador para registrar acciones de auditoría (crear, modificar, eliminar, visualizar).

    Determina automáticamente el modelo y el objeto afectado y crea una
    entrada en el modelo Auditoria si la operación es exitosa.
    También captura la dirección IP y el User-Agent del navegador.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            instance_representation = ""
            # Para 'update' y 'destroy', obtenemos el estado del objeto *antes* de la acción.
            if func.__name__ in ['update', 'partial_update', 'destroy']:
                try:
                    instance = self.get_object()
                    instance_representation = str(instance)
                except Exception:
                    # Si get_object falla, la vista manejará el error.
                    pass

            # Ejecutar la función original de la vista
            response = func(self, request, *args, **kwargs)

            # Solo registrar si la respuesta fue exitosa (códigos 2xx)
            if 200 <= response.status_code < 300:
                model_name = ""
                if hasattr(self, 'queryset') and self.queryset is not None:
                    model_name = self.queryset.model._meta.verbose_name.title()
                
                # Para 'create', el objeto se representa desde los datos de la respuesta.
                if func.__name__ == 'create' and hasattr(response, 'data'):
                    # Intentamos obtener una representación legible
                    if 'nombre' in response.data:
                        instance_representation = response.data.get('nombre')
                    elif 'name' in response.data:
                        instance_representation = response.data.get('name')
                    elif 'id' in response.data:
                        instance_representation = f"ID {response.data.get('id')}"
                    else:
                        # Fallback a una representación genérica si no se encuentran campos comunes
                        instance_representation = "nuevo registro"

                # Construir el mensaje de acción
                if func.__name__ == 'list':
                    accion = f"{action_verb} la lista de {model_name}"
                else:
                    accion = f"{action_verb} el {model_name}: '{instance_representation}'"
                
                # Obtener IP y User-Agent
                direccion_ip = request.META.get('REMOTE_ADDR')
                navegador = request.META.get('HTTP_USER_AGENT', 'Desconocido')

                # Crear la entrada de auditoría
                Auditoria.objects.create(
                    usuario=request.user,
                    accion=accion,
                    direccion_ip=direccion_ip,
                    navegador=navegador
                )

            return response
        return wrapper
    return decorator