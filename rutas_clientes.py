# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de clientes
# "rutas_clientes" es el nombre del módulo
# __name__ permite ubicar las plantillas dentro del proyecto
rutas_clientes = Blueprint("rutas_clientes", __name__)

# URL base de la API en C# que gestiona los clientes
API_URL = "http://localhost:5031/api/cliente"

# ------------------- LISTAR clientes -------------------
@rutas_clientes.route("/clientes")
def clientes():
    """
    Ruta para listar todos los clientes disponibles en la API.
    Llama al endpoint /api/cliente y extrae la lista de clientes desde la clave "datos".
    """
    try:
        respuesta = requests.get(API_URL)
        clientes = respuesta.json().get("datos", [])
    except Exception as e:
        clientes = []
        print("Error al conectar con la API:", e)

    # Retorna la plantilla clientes.html con la lista de clientes
    return render_template(
        "clientes.html",
        clientes=clientes,
        cliente=None,
        modo="crear"
    )

# ------------------- BUSCAR cliente -------------------
@rutas_clientes.route("/clientes/buscar", methods=["POST"])
def buscar_cliente():
    """
    Ruta para buscar un cliente específico a partir de su código.
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
                    # Si la API retorna datos, se asume que es una lista con un cliente
                    cliente = datos[0]
                    clientes = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "clientes.html",
                        clientes=clientes,
                        cliente=cliente,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra el cliente, recargar la lista completa
    clientes = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "clientes.html",
        clientes=clientes,
        cliente=None,
        mensaje="Cliente no encontrado",
        modo="crear"
    )

# ------------------- CREAR cliente -------------------
@rutas_clientes.route("/clientes/crear", methods=["POST"])
def crear_cliente():
    """
    Ruta para crear un cliente nuevo en la API.
    Toma los datos del formulario y los envía vía POST al endpoint /api/cliente.
    """
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre"),
        "correo": request.form.get("correo"),
        "telefono": request.form.get("telefono")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear cliente: {e}"

    return redirect(url_for("rutas_clientes.clientes"))

# ------------------- ACTUALIZAR cliente -------------------
@rutas_clientes.route("/clientes/actualizar", methods=["POST"])
def actualizar_cliente():
    """
    Ruta para actualizar un cliente existente en la API.
    Busca por código y realiza una petición PUT con los nuevos datos.
    """
    codigo = request.form.get("codigo")
    datos = {
        "nombre": request.form.get("nombre"),
        "correo": request.form.get("correo"),
        "telefono": request.form.get("telefono")
    }

    try:
        requests.put(f"{API_URL}/codigo/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar cliente: {e}"

    return redirect(url_for("rutas_clientes.clientes"))

# ------------------- ELIMINAR cliente -------------------
@rutas_clientes.route("/clientes/eliminar/<string:codigo>", methods=["POST"])
def eliminar_cliente(codigo):
    """
    Ruta para eliminar un cliente de la API según su código.
    Envía una petición DELETE al endpoint correspondiente.
    """
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar cliente: {e}"

    return redirect(url_for("rutas_clientes.clientes"))
