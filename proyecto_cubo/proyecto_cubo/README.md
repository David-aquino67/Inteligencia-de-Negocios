# Proyecto: Simulador de Cubo OLAP con Flask

Este proyecto implementa una aplicación web local que demuestra las
operaciones OLAP (Slice, Dice, Drill-through) utilizando Pandas para
el procesamiento de datos y Flask para la visualización.

## 1. Verificación de Ejecución

El script `usocubos.py` (el punto de acceso original) fue verificado
y sus funciones fueron migradas al servidor web `app.py`. El script
`app.py` ahora sirve como el punto de acceso principal.

## 2. Implementación de la Página Web

La aplicación web (`app.py`) cumple con todos los requisitos solicitados.

### Estructura de Funciones (Requisito 2)

La página principal (`/`) muestra una sección que detalla la
estructura del proyecto, explicando el rol de cada archivo:
* `app.py`: Servidor web Flask.
* `funciones/generarDatos.py`: Crea el DataFrame de datos crudos.
* `funciones/crearCubo.py`: Define las vistas de tabla pivote.
* `funciones/operacionesCubo.py`: Contiene las lógicas de filtrado (slice, dice).

### Visualización del Cubo (Requisito 3)

La página principal también visualiza:

* **El Cubo Completo:** Una tabla pivote (Producto/Región vs. Año/Trimestre)
    generada por `cubo_base()`.
* **Una Cara del Cubo (Slice):** Una vista filtrada que muestra
    solo los datos del año 2024, generada por `slice_por_anio()`.
* **Una Sección del Cubo (Dice):** Una vista de los datos crudos
    filtrados por (Años 2024-2025) y (Regiones Norte-Sur),
    generada por `dice_subset()`.

### Datos de una Celda (Drill-Through)

La página principal incluye un formulario para seleccionar las
coordenadas de una celda (Producto, Región, Año, Trimestre).
Al enviar, se redirige a la página `/celda`, que muestra todos
los registros de la base de datos cruda que componen el valor
total de esa celda específica.

## 3. Cómo Ejecutar

1.  Asegurarse de tener `pandas`, `numpy` y `flask` instalados:
    ```bash
    pip install pandas numpy flask
    ```
2.  Navegar a la carpeta raíz del proyecto.
3.  Ejecutar el servidor Flask:
    ```bash python app.py 
    ```
4.  Abrir un navegador y visitar: `http://127.0.0.1:5000`