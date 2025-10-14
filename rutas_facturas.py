# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de facturas
# "rutas_facturas" es el nombre del módulo
# __name__ permite ubicar las plantillas dentro del proyecto
rutas_facturas = Blueprint("rutas_facturas", __name__)

# URL base de la API en C# que gestiona las facturas
API_URL = "http://localhost:5031/api/factura"

# ------------------- LISTAR facturas -------------------
@rutas_facturas.route("/facturas")
def facturas():
    """
    Ruta para listar todas las facturas disponibles en la API.
    Llama al endpoint /api/factura y extrae la lista de facturas desde la clave "datos".
    """
    try:
        respuesta = requests.get(API_URL)
        facturas = respuesta.json().get("datos", [])
    except Exception as e:
        facturas = []
        print("Error al conectar con la API:", e)

    # Retorna la plantilla facturas.html con la lista de facturas
    return render_template(
        "facturas.html",
        facturas=facturas,
        factura=None,
        modo="crear"
    )

# ------------------- BUSCAR factura -------------------
@rutas_facturas.route("/facturas/buscar", methods=["POST"])
def buscar_factura():
    """
    Ruta para buscar una factura específica a partir de su código.
    Si la encuentra, carga sus datos en el formulario en modo "actualizar".
    Si no existe, retorna un mensaje y la lista completa.
    """
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/codigo/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    # Si la API retorna datos, se asume que es una lista con una factura
                    factura = datos[0]
                    facturas = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "facturas.html",
                        facturas=facturas,
                        factura=factura,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra la factura, recargar la lista completa
    facturas = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "facturas.html",
        facturas=facturas,
        factura=None,
        mensaje="Factura no encontrada",
        modo="crear"
    )

# ------------------- CREAR factura -------------------
@rutas_facturas.route("/facturas/crear", methods=["POST"])
def crear_factura():
    """
    Ruta para crear una factura nueva en la API.
    Toma los datos del formulario y los envía vía POST al endpoint /api/factura.
    """
    datos = {
        "codigo": request.form.get("codigo"),
        "fecha": request.form.get("fecha"),
        "cliente": request.form.get("cliente"),
        "total": float(request.form.get("total", 0))
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear factura: {e}"

    return redirect(url_for("rutas_facturas.facturas"))

# ------------------- ACTUALIZAR factura -------------------
@rutas_facturas.route("/facturas/actualizar", methods=["POST"])
def actualizar_factura():
    """
    Ruta para actualizar una factura existente en la API.
    Busca por código y realiza una petición PUT con los nuevos datos.
    """
    codigo = request.form.get("codigo")
    datos = {
        "fecha": request.form.get("fecha"),
        "cliente": request.form.get("cliente"),
        "total": float(request.form.get("total", 0))
    }

    try:
        requests.put(f"{API_URL}/codigo/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar factura: {e}"

    return redirect(url_for("rutas_facturas.facturas"))

# ------------------- ELIMINAR factura -------------------
@rutas_facturas.route("/facturas/eliminar/<string:codigo>", methods=["POST"])
def eliminar_factura(codigo):
    """
    Ruta para eliminar una factura de la API según su código.
    Envía una petición DELETE al endpoint correspondiente.
    """
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar factura: {e}"

    return redirect(url_for("rutas_facturas.facturas"))
