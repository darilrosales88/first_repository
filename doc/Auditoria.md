# Documentación del Decorador de Auditoría (`@audit_log`)

## 1. Introducción

Para estandarizar y simplificar el registro de acciones en el sistema, se ha introducido un decorador llamado `@audit_log`. Anteriormente, el registro de auditoría se realizaba manualmente en cada método de las vistas (`create`, `update`, `destroy`, `list`), lo que resultaba en código repetitivo y propenso a errores.

El nuevo decorador centraliza esta lógica, haciendo que el código sea más limpio, mantenible y consistente.

## 2. ¿Cómo funciona?

El decorador `@audit_log` envuelve los métodos de un `ViewSet` de Django Rest Framework. Automáticamente:

1.  Ejecuta la acción solicitada (crear, modificar, etc.).
2.  Verifica si la operación fue exitosa (códigos de estado HTTP `2xx`).
3.  Si la operación tuvo éxito, crea un registro en el modelo `Auditoria`.
4.  Extrae automáticamente el **usuario**, el **nombre del modelo** y el **objeto afectado** para construir un mensaje de auditoría descriptivo.

## 3. ¿Cómo usarlo?

Para utilizar el decorador, sigue estos pasos:

### Paso 1: Importar el decorador

En tu archivo `views.py`, importa el decorador desde `nomencladores.decorators`:

```python
from Administracion.decorators import audit_log
```

### Paso 2: Aplicar el decorador a los métodos del ViewSet

Añade el decorador justo encima de los métodos que deseas auditar (`create`, `update`, `destroy`, `list`). Debes pasarle como argumento el verbo que describe la acción.

**Ejemplo completo de un `ViewSet` refactorizado:**

```python
from rest_framework import viewsets
from .models import nom_pais
from .serializers import nom_pais_serializer
from .decorators import audit_log
from .permissions import IsAdminNomenladoresPermission, IsVisualizadorNomencladoresPermission

class nom_pais_view_set(viewsets.ModelViewSet):
    queryset = nom_pais.objects.all().order_by('-id')
    serializer_class = nom_pais_serializer
    # Los permisos ahora se gestionan a nivel de clase para simplificar
    permission_classes = [IsAdminNomenladoresPermission | IsVisualizadorNomencladoresPermission]

    def get_queryset(self):
        # ... (lógica de filtrado sin cambios)
        return super().get_queryset()
    
    @audit_log("Crear")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @audit_log("Modificar")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @audit_log("Eliminar")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @audit_log("Visualizar")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

### Argumentos del decorador

El decorador recibe un único argumento:

-   `action_verb` (cadena de texto): El verbo que describe la acción. Ejemplos: `"Crear"`, `"Modificar"`, `"Eliminar"`, `"Visualizar"`.

El mensaje final se construirá automáticamente. Por ejemplo, para `@audit_log("Crear")` en el `nom_pais_view_set`, el mensaje de auditoría será: `Crear el País: 'Cuba'`.

## 4. Beneficios

-   **Código Limpio y DRY (Don't Repeat Yourself):** Elimina docenas de líneas de código repetido.
-   **Consistencia:** Asegura que todos los mensajes de auditoría sigan el mismo formato.
-   **Mantenibilidad:** Si se necesita cambiar la lógica de auditoría, solo se debe modificar el decorador en un único lugar.
-   **Fiabilidad:** El registro solo ocurre si la operación principal (crear, modificar, etc.) se completa con éxito.

A partir de ahora, todo el equipo debe adoptar este enfoque para el registro de auditoría en las nuevas vistas que se desarrollen.
