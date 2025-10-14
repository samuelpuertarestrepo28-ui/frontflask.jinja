# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de vendedores
# "rutas_vendedores" es el nombre del módulo
# __name__ permite ubicar las plantillas dentro del proyecto
rutas_vendedores = Blueprint("rutas_vendedores", __name__)

# URL base de la API en C# que gestiona los vendedores
API_URL = "http://localhost:5031/api/vendedor"

# ------------------- LISTAR vendedores -------------------
@rutas_vendedores.route("/vendedores")
def vendedores():
    """
    Ruta para listar todos los vendedores disponibles en la API.
    Llama al endpoint /api/vendedor y extrae la lista de vendedores desde la clave "datos".
    """
    try:
        respuesta = requests.get(API_URL)
        vendedores = respuesta.json().get("datos", [])
    except Exception as e:
        vendedores = []
        print("Error al conectar con la API:", e)

    # Retorna la plantilla vendedores.html con la lista de vendedores
    return render_template(
        "vendedores.html",
        vendedores=vendedores,
        vendedor=None,
        modo="crear"
    )

# ------------------- BUSCAR vendedor -------------------
@rutas_vendedores.route("/vendedores/buscar", methods=["POST"])
def buscar_vendedor():
    """
    Ruta para buscar un vendedor específico a partir de su código.
    Si lo encuentra, carga sus datos en el formulario en modo "actualizar".
    Si no existe, retorna un mensaje y la lista completa.
    """
    codigo = request.form.get("codigo_buscar")

    if codigo:
        try:
            respuesta = requests.get(f"{API_URL}/codigo/{codigo}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    # Si la API retorna datos, se asume que es una lista con un vendedor
                    vendedor = datos[0]
                    vendedores = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "vendedores.html",
                        vendedores=vendedores,
                        vendedor=vendedor,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra el vendedor, recargar la lista completa
    vendedores = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "vendedores.html",
        vendedores=vendedores,
        vendedor=None,
        mensaje="Vendedor no encontrado",
        modo="crear"
    )

# ------------------- CREAR vendedor -------------------
@rutas_vendedores.route("/vendedores/crear", methods=["POST"])
def crear_vendedor():
    """
    Ruta para crear un vendedor nuevo en la API.
    Toma los datos del formulario y los envía vía POST al endpoint /api/vendedor.
    """
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre"),
        "telefono": request.form.get("telefono")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear vendedor: {e}"

    return redirect(url_for("rutas_vendedores.vendedores"))

# ------------------- ACTUALIZAR vendedor -------------------
@rutas_vendedores.route("/vendedores/actualizar", methods=["POST"])
def actualizar_vendedor():
    """
    Ruta para actualizar un vendedor existente en la API.
    Busca por código y realiza una petición PUT con los nuevos datos.
    """
    codigo = request.form.get("codigo")
    datos = {
        "nombre": request.form.get("nombre"),
        "telefono": request.form.get("telefono")
    }

    try:
        requests.put(f"{API_URL}/codigo/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar vendedor: {e}"

    return redirect(url_for("rutas_vendedores.vendedores"))

# ------------------- ELIMINAR vendedor -------------------
@rutas_vendedores.route("/vendedores/eliminar/<string:codigo>", methods=["POST"])
def eliminar_vendedor(codigo):
    """
    Ruta para eliminar un vendedor de la API según su código.
    Envía una petición DELETE al endpoint correspondiente.
    """
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar vendedor: {e}"

    return redirect(url_for("rutas_vendedores.vendedores"))
