from flask import Flask, render_template, request
import pandas as pd 
from funciones.generarDatos import generar_dataset
from funciones.crearCubo import cubo_base
from funciones.operacionesCubo import slice_por_anio, dice_subset

app = Flask(__name__)

print("Generando dataset y cubo base...")
df_crudo = generar_dataset()
cubo = cubo_base(df_crudo)
print("¡Servidor listo!")


@app.route('/')
def index():
    return render_template('menu.html')


@app.route('/cubo')
def cubo_completo():
    cubo_html = cubo.to_html(classes='table table-striped table-hover', border=0)
    return render_template('vista.html', titulo="El Cubo Completo", contenido=cubo_html)


@app.route('/cara')
def cara_cubo():
    anio = request.args.get('anio', default=2024, type=int)
    cara = slice_por_anio(df_crudo, anio)
    cara_html = pd.pivot_table(
        cara,
        values="Ventas",
        index="Producto",
        columns="Región",
        aggfunc="sum",
        margins=True
    ).to_html(classes='table table-striped table-hover', border=0)

    return render_template(
        'vista.html',
        titulo=f"Una Cara del Cubo (Año {anio})",
        contenido=cara_html,
        mostrar_formulario_cara=True
    )


@app.route('/seccion')
def seccion_cubo():
    anios_param = request.args.get('anios')
    regiones_param = request.args.get('regiones')
    productos_param = request.args.get('productos')
    canales_param = request.args.get('canales')

    anios = [int(a) for a in anios_param.split(',')] if anios_param else None
    regiones = regiones_param.split(',') if regiones_param else None
    productos = productos_param.split(',') if productos_param else None
    canales = canales_param.split(',') if canales_param else None

    seccion_subset = dice_subset(df_crudo, anios=anios, regiones=regiones,
                                 productos=productos, canales=canales)

    if seccion_subset.empty:
        seccion_html = "<p class='text-danger'>No hay datos para los filtros seleccionados.</p>"
    else:
        seccion_html = seccion_subset.head(30).to_html(
            classes='table table-bordered table-hover table-sm shadow-sm',
            border=0, index=False
        )

    filtros_usados = []
    if anios: filtros_usados.append(f"Años={anios}")
    if regiones: filtros_usados.append(f"Regiones={regiones}")
    if productos: filtros_usados.append(f"Productos={productos}")
    if canales: filtros_usados.append(f"Canales={canales}")
    filtros_str = ", ".join(filtros_usados) if filtros_usados else "Sin filtros"

    return render_template(
        'vista.html',
        titulo="Una Sección del Cubo",
        contenido=seccion_html,
        mostrar_formulario_seccion=True
    )

@app.route('/celda')
def ver_celda():
    try:
        producto = request.args.get('producto')
        region = request.args.get('region')
        anio = request.args.get('anio')
        trimestre = request.args.get('trimestre')

        if not all([producto, region, anio, trimestre]):
            return render_template('celda.html', datos_celda=None, params=None)

        anio = int(anio)
        trimestre = int(trimestre)

        filtro = (
            (df_crudo['Producto'] == producto) &
            (df_crudo['Región'] == region) &
            (df_crudo['Año'] == anio) &
            (df_crudo['Trimestre'] == trimestre)
        )

        datos_celda = df_crudo[filtro]
        params_str = f"Producto={producto}, Región={region}, Año={anio}, Trimestre={trimestre}"

        if datos_celda.empty:
            datos_html = "<p>No se encontraron datos para esta celda.</p>"
        else:
            datos_html = datos_celda.to_html(classes='table table-striped table-hover', border=0, index=False)

        return render_template('celda.html', datos_celda=datos_html, params=params_str)

    except Exception as e:
        return f"Error al procesar la solicitud: {e}"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
