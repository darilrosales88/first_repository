# base-frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### NOTAS CARLOS: ATENTO
- El boton de Rotacion no pregunta los permisos del usuario, deberia aparecer solo cuando el usuario pertenece al grupo  ("AdminUFC","OperadorUFC")

- Se hacen llamadas al backend en muchas ocaciones para obtener el grupo al que pertence el usuario,
Esto se pudiera evitar si de alguna manera se guardara en el localstorage de la pagina, haciendo una sola llamada en el componte informeOperativoVIEW padre y luego se le pasara como props a los componentes hijos, de los 5 estados y rotaciones y vagones y productos.

- En el editar del arrastre se pone el tipo de equipo pero no se ve el id ni la diferencia que puee haber entre uno u otro.

### Sobre el tiempo de respuesta al crear un usuario, 
- [21/Jul/2025 22:09:01] "POST /apiAdmin/creacion-usuario/ HTTP/1.1" 201 "41" -> Este ultimo valor es el tiempo de respuesta en ms.