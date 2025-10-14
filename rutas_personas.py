# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de personas
# "rutas_personas" es el nombre del módulo
# __name__ permite ubicar las plantillas dentro del proyecto
rutas_personas = Blueprint("rutas_personas", __name__)

# URL base de la API en C# que gestiona las personas
API_URL = "http://localhost:5031/api/persona"

# ------------------- LISTAR personas -------------------
@rutas_personas.route("/personas")
def personas():
    """
    Ruta para listar todas las personas disponibles en la API.
    Llama al endpoint /api/persona y extrae la lista de personas desde la clave "datos".
    """
    try:
        respuesta = requests.get(API_URL)
        personas = respuesta.json().get("datos", [])
    except Exception as e:
        personas = []
        print("Error al conectar con la API:", e)

    # Retorna la plantilla personas.html con la lista de personas
    return render_template(
        "personas.html",
        personas=personas,
        persona=None,
        modo="crear"
    )

# ------------------- BUSCAR persona -------------------
@rutas_personas.route("/personas/buscar", methods=["POST"])
def buscar_persona():
    """
    Ruta para buscar una persona específica a partir de su código.
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
                    # Si la API retorna datos, se asume que es una lista con una persona
                    persona = datos[0]
                    personas = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "personas.html",
                        personas=personas,
                        persona=persona,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra la persona, recargar la lista completa
    personas = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "personas.html",
        personas=personas,
        persona=None,
        mensaje="Persona no encontrada",
        modo="crear"
    )

# ------------------- CREAR persona -------------------
@rutas_personas.route("/personas/crear", methods=["POST"])
def crear_persona():
    """
    Ruta para crear una persona nueva en la API.
    Toma los datos del formulario y los envía vía POST al endpoint /api/persona.
    """
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre"),
        "telefono": request.form.get("telefono")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear persona: {e}"

    return redirect(url_for("rutas_personas.personas"))

# ------------------- ACTUALIZAR persona -------------------
@rutas_personas.route("/personas/actualizar", methods=["POST"])
def actualizar_persona():
    """
    Ruta para actualizar una persona existente en la API.
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
        return f"Error al actualizar persona: {e}"

    return redirect(url_for("rutas_personas.personas"))

# ------------------- ELIMINAR persona -------------------
@rutas_personas.route("/personas/eliminar/<string:codigo>", methods=["POST"])
def eliminar_persona(codigo):
    """
    Ruta para eliminar una persona de la API según su código.
    Envía una petición DELETE al endpoint correspondiente.
    """
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar persona: {e}"

    return redirect(url_for("rutas_personas.personas"))
