<template>
    <div style="background-color: #002A68; color: white; text-align: right; padding: 10px;">
      <h6>Bienvenido: {{ username }}</h6>
    </div>
    <br />
    <Navbar-Component /><br>

    <div class="carrusel">
        <!-- Tabla 1 -->
        <div class="tabla activa">
            <table>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Edad</th>
                        <th>Ciudad</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Juan</td>
                        <td>25</td>
                        <td>Madrid</td>
                    </tr>
                    <tr>
                        <td>Ana</td>
                        <td>30</td>
                        <td>Barcelona</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Tabla 2 -->
        <div class="tabla">
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Precio</th>
                        <th>Stock</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Laptop</td>
                        <td>$1200</td>
                        <td>10</td>
                    </tr>
                    <tr>
                        <td>Teléfono</td>
                        <td>$800</td>
                        <td>15</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Tabla 3 -->
        <div class="tabla">
            <table>
                <thead>
                    <tr>
                        <th>País</th>
                        <th>Capital</th>
                        <th>Población</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>España</td>
                        <td>Madrid</td>
                        <td>47M</td>
                    </tr>
                    <tr>
                        <td>México</td>
                        <td>CDMX</td>
                        <td>126M</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Controles de navegación -->
    <button id="anterior">Anterior</button>
    <button id="siguiente">Siguiente</button>

    <!-- Indicadores -->
    <div class="indicadores">
        <span class="indicador activo"></span>
        <span class="indicador"></span>
        <span class="indicador"></span>
    </div>


</template>

<style scoped>
/* styles.css */
body {
    font-family: Arial, sans-serif;
    text-align: center;
}

.carrusel {
    position: relative;
    width: 80%;
    margin: 0 auto;
    overflow: hidden;
}

.tabla {
    display: none; /* Oculta todas las tablas por defecto */
    width: 100%;
    margin: 20px 0;
    opacity: 0;
    transition: opacity 0.5s ease-in-out; /* Transición suave */
}

.tabla.activa {
    display: block; /* Muestra solo la tabla activa */
    opacity: 1; /* Hace visible la tabla activa */
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f4f4f4;
}

button {
    padding: 10px 20px;
    margin: 10px;
    cursor: pointer;
}

.indicadores {
    margin-top: 20px;
}

.indicador {
    display: inline-block;
    width: 10px;
    height: 10px;
    background-color: #bbb;
    border-radius: 50%;
    margin: 0 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.indicador.activo {
    background-color: #333; /* Color para el indicador activo */
}
</style>

<script>
    const tablas = document.querySelectorAll('.tabla');
const btnAnterior = document.getElementById('anterior');
const btnSiguiente = document.getElementById('siguiente');
const indicadores = document.querySelectorAll('.indicador');
let indiceActual = 0;

// Función para mostrar la tabla actual
function mostrarTabla(indice) {
    // Oculta todas las tablas
    tablas.forEach((tabla) => {
        tabla.classList.remove('activa');
    });

    // Muestra la tabla actual
    tablas[indice].classList.add('activa');

    // Actualiza los indicadores
    indicadores.forEach((indicador, i) => {
        if (i === indice) {
            indicador.classList.add('activo');
        } else {
            indicador.classList.remove('activo');
        }
    });
}

// Evento para el botón "Siguiente"
btnSiguiente.addEventListener('click', () => {
    indiceActual = (indiceActual + 1) % tablas.length;
    mostrarTabla(indiceActual);
});

// Evento para el botón "Anterior"
btnAnterior.addEventListener('click', () => {
    indiceActual = (indiceActual - 1 + tablas.length) % tablas.length;
    mostrarTabla(indiceActual);
});

// Evento para los indicadores
indicadores.forEach((indicador, i) => {
    indicador.addEventListener('click', () => {
        indiceActual = i;
        mostrarTabla(indiceActual);
    });
});

// Mostrar la primera tabla al cargar la página
mostrarTabla(indiceActual);
</script>