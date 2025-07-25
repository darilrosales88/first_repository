# Desglose de Requisitos Funcionales (RF) del Documento

## Agrupación: Gestionar tipo de parte CCD por producto

---

### RF1: Consultar tipo de parte CCD por producto

- **Descripción:** Visualizar registros de partes CCD por producto.
- **Campos:** Fecha operación, Fecha actual, Comentarios.
- **Validaciones:** Paginación (10 elementos), cálculos automáticos de totales.
- **Prioridad:** M (Media).

---

### RF2: Adicionar parte CCD por producto

- **Descripción:** Crear nuevos partes CCD por producto.
- **Campos obligatorios:** Fecha operación (única), Comentarios (opcional).
- **Validaciones:** Cálculos automáticos (ej. Total General = Total Ayer + Entro hoy).
- **Mensajes:** Confirmación de creación/error.
- **Prioridad:** M.

---

### RF3: Editar parte CCD por producto

- **Descripción:** Modificar partes existentes en estado "CREADO".
- **Validaciones:** Restricciones de unicidad en campos, validación de campos obligatorios.
- **Mensajes:** Alertas de error/éxito.
- **Prioridad:** M.

---

## Agrupación: Gestionar datos generales del CCD

---

### RF4: Listar datos generales del CCD

- **Descripción:** Mostrar datos generales asociados a un parte CCD.
- **Campos:** Acceso comercial, Total ayer, Entro hoy, etc.
- **Validaciones:** Paginación, cálculos automáticos (ej. Diferencia carga = Real carga – Plan carga).
- **Prioridad:** M.

---

### RF5: Adicionar datos generales del CCD

- **Descripción:** Añadir registros de datos generales a un parte CCD.
- **Campos obligatorios:** Acceso comercial, Total ayer, Entro hoy, Plan carga, Plan descarga.
- **Validaciones:** Cálculos en tiempo real, unicidad de campos.
- **Prioridad:** M.

---

### RF6: Editar datos generales CCD

- **Descripción:** Modificar datos generales existentes.
- **Validaciones:** Actualización automática de campos calculados.
- **Prioridad:** M.

---

### RF7: Eliminar registro datos generales del CCD

- **Descripción:** Eliminar registros de datos generales.
- **Mensajes:** Confirmación de eliminación.
- **Prioridad:** M.

---

### RF8: Buscar datos generales del CCD

- **Descripción:** Búsqueda por producto/origen.
- **Mensajes:** Notificación si no hay resultados.
- **Prioridad:** M.

---

## Agrupación: Gestionar cargas pendientes de arrastre del CCD

---

### RF9: Listar cargas pendientes de arrastre del CCD

- **Descripción:** Mostrar cargas pendientes de arrastre.
- **Campos:** Tipo equipo, Estado, Producto, Cantidad vagones.
- **Prioridad:** M.

---

### RF10: Adicionar cargas pendientes de arrastre del CCD

- **Descripción:** Añadir nuevas cargas pendientes.
- **Campos clave:** Acceso comercial, Tipo equipo, Estado, No. ID (único).
- **Validaciones:** Combinaciones únicas de campos.
- **Prioridad:** M.

---

### RF11: Editar cargas pendientes de arrastre del CCD

- **Descripción:** Modificar cargas pendientes existentes.
- **Validaciones:** Restricciones de unicidad y campos obligatorios.
- **Prioridad:** M.

---

### RF12: Eliminar cargas pendientes de arrastre

- **Descripción:** Eliminar registros.
- **Mensajes:** Confirmación.
- **Prioridad:** M.

---

### RF13: Buscar cargas pendientes de arrastre

- **Descripción:** Búsqueda por producto/origen.
- **Prioridad:** M.

---

## Agrupación: Gestionar cargas en trenes del CCD

---

### RF14: Listar cargas en trenes del CCD

- **Descripción:** Mostrar cargas en trenes.
- **Campos:** Locomotora, Tipo equipo, Producto.
- **Prioridad:** M.

---

### RF15: Adicionar cargas en trenes del CCD

- **Descripción:** Añadir cargas en trenes.
- **Campos clave:** Acceso comercial, Tipo equipo, Estado, No. ID (único).
- **Prioridad:** M.

---

### RF16: Editar cargas en trenes del CCD

- **Descripción:** Modificar cargas en trenes.
- **Validaciones:** Campos obligatorios y únicos.
- **Prioridad:** M.

---

### RF17: Eliminar cargas en trenes

- **Descripción:** Eliminar registros.
- **Prioridad:** M.

---

### RF18: Buscar cargas en trenes

- **Descripción:** Búsqueda por producto/origen.
- **Prioridad:** M.

---

## Agrupación: Gestionar vagones cargados/descargados del CCD

---

### RF19: Listar vagones cargados/descargados del CCD

- **Descripción:** Mostrar vagones cargados/descargados.
- **Campos:** Tipo equipo, Operación, Producto, Incidencia.
- **Prioridad:** M.

---

### RF20: Adicionar vagones cargados/descargados del CCD

- **Descripción:** Añadir vagones cargados/descargados.
- **Campos clave:** Acceso comercial, Tipo equipo, Operación, Producto.
- **Validaciones:** Combinaciones únicas de campos.
- **Prioridad:** M.

---

### RF21: Editar vagones cargados/descargados del CCD

- **Descripción:** Modificar registros existentes.
- **Validaciones:** Restricciones de unicidad.
- **Prioridad:** M.

---

### RF22: Eliminar vagones cargados/descargados

- **Descripción:** Eliminar registros.
- **Prioridad:** M.

---

## Resumen de Características Comunes

- **Roles:** Todos los RF requieren usuario autenticado con rol ufc.
- **Complejidad:** Baja para todos los RF.
- **Prioridad:** Media (M) para todos.

### Patrones Comunes

- Paginación en listados (máx. 10 elementos).
- Validaciones de campos únicos/obligatorios.
- Mensajes de confirmación/error.
- Cálculos automáticos (ej. totales, diferencias).

**Dependencias:** Varios RF ejecutan otros RF (ej. RF2 invoca RF5, RF10, etc.).

> Este desglose organiza los 22 RF en agrupaciones temáticas, destacando funcionalidades clave y relaciones entre ellos.
