# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de empresas
# "rutas_empresas" es el nombre del módulo
# __name__ permite ubicar las plantillas dentro del proyecto
rutas_empresas = Blueprint("rutas_empresas", __name__)

# URL base de la API en C# que gestiona las empresas
API_URL = "http://localhost:5031/api/empresa"

# ------------------- LISTAR empresas -------------------
@rutas_empresas.route("/empresas")
def empresas():
    """
    Ruta para listar todas las empresas disponibles en la API.
    Llama al endpoint /api/empresa y extrae la lista de empresas desde la clave "datos".
    """
    try:
        respuesta = requests.get(API_URL)
        empresas = respuesta.json().get("datos", [])
    except Exception as e:
        empresas = []
        print("Error al conectar con la API:", e)

    # Retorna la plantilla empresas.html con la lista de empresas
    return render_template(
        "empresas.html",
        empresas=empresas,
        empresa=None,
        modo="crear"
    )

# ------------------- BUSCAR empresa -------------------
@rutas_empresas.route("/empresas/buscar", methods=["POST"])
def buscar_empresa():
    """
    Ruta para buscar una empresa específica a partir de su código.
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
                    # Si la API retorna datos, se asume que es una lista con una empresa
                    empresa = datos[0]
                    empresas = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "empresas.html",
                        empresas=empresas,
                        empresa=empresa,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra la empresa, recargar la lista completa
    empresas = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "empresas.html",
        empresas=empresas,
        empresa=None,
        mensaje="Empresa no encontrada",
        modo="crear"
    )

# ------------------- CREAR empresa -------------------
@rutas_empresas.route("/empresas/crear", methods=["POST"])
def crear_empresa():
    """
    Ruta para crear una empresa nueva en la API.
    Toma los datos del formulario y los envía vía POST al endpoint /api/empresa.
    """
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre"),
        "telefono": request.form.get("telefono")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear empresa: {e}"

    return redirect(url_for("rutas_empresas.empresas"))

# ------------------- ACTUALIZAR empresa -------------------
@rutas_empresas.route("/empresas/actualizar", methods=["POST"])
def actualizar_empresa():
    """
    Ruta para actualizar una empresa existente en la API.
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
        return f"Error al actualizar empresa: {e}"

    return redirect(url_for("rutas_empresas.empresas"))

# ------------------- ELIMINAR empresa -------------------
@rutas_empresas.route("/empresas/eliminar/<string:codigo>", methods=["POST"])
def eliminar_empresa(codigo):
    """
    Ruta para eliminar una empresa de la API según su código.
    Envía una petición DELETE al endpoint correspondiente.
    """
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar empresa: {e}"

    return redirect(url_for("rutas_empresas.empresas"))
