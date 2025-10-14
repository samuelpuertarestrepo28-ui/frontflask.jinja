# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Crear el Blueprint de productos
# "rutas_productos" es el nombre del módulo
# __name__ permite ubicar las plantillas dentro del proyecto
rutas_productos = Blueprint("rutas_productos", __name__)

# URL base de la API en C# que gestiona los productos
API_URL = "http://localhost:5031/api/producto"

# ------------------- LISTAR productos -------------------
@rutas_productos.route("/productos")
def productos():
    """
    Ruta para listar todos los productos disponibles en la API.
    Llama al endpoint /api/producto y extrae la lista de productos desde la clave "datos".
    """
    try:
        respuesta = requests.get(API_URL)
        productos = respuesta.json().get("datos", [])
    except Exception as e:
        productos = []
        print("Error al conectar con la API:", e)

    # Retorna la plantilla productos.html con la lista de productos
    return render_template(
        "productos.html",
        productos=productos,
        producto=None,
        modo="crear"
    )

# ------------------- BUSCAR producto -------------------
@rutas_productos.route("/productos/buscar", methods=["POST"])
def buscar_producto():
    """
    Ruta para buscar un producto específico a partir de su código.
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
                    # Si la API retorna datos, se asume que es una lista con un producto
                    producto = datos[0]
                    productos = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "productos.html",
                        productos=productos,
                        producto=producto,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra el producto, recargar la lista completa
    productos = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "productos.html",
        productos=productos,
        producto=None,
        mensaje="Producto no encontrado",
        modo="crear"
    )

# ------------------- CREAR producto -------------------
@rutas_productos.route("/productos/crear", methods=["POST"])
def crear_producto():
    """
    Ruta para crear un producto nuevo en la API.
    Toma los datos del formulario y los envía vía POST al endpoint /api/producto.
    """
    datos = {
        "codigo": request.form.get("codigo"),
        "nombre": request.form.get("nombre"),
        "valorunitario": int(request.form.get("valorunitario", 0)),
        "stock": int(request.form.get("stock", 0))
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear producto: {e}"

    return redirect(url_for("rutas_productos.productos"))

# ------------------- ACTUALIZAR producto -------------------
@rutas_productos.route("/productos/actualizar", methods=["POST"])
def actualizar_producto():
    """
    Ruta para actualizar un producto existente en la API.
    Busca por código y realiza una petición PUT con los nuevos datos.
    """
    codigo = request.form.get("codigo")
    datos = {
        "nombre": request.form.get("nombre"),
        "valorunitario": int(request.form.get("valorunitario", 0)),
        "stock": int(request.form.get("stock", 0))
    }

    try:
        requests.put(f"{API_URL}/codigo/{codigo}", json=datos)
    except Exception as e:
        return f"Error al actualizar producto: {e}"

    return redirect(url_for("rutas_productos.productos"))

# ------------------- ELIMINAR producto -------------------
@rutas_productos.route("/productos/eliminar/<string:codigo>", methods=["POST"])
def eliminar_producto(codigo):
    """
    Ruta para eliminar un producto de la API según su código.
    Envía una petición DELETE al endpoint correspondiente.
    """
    try:
        requests.delete(f"{API_URL}/codigo/{codigo}")
    except Exception as e:
        return f"Error al eliminar producto: {e}"

    return redirect(url_for("rutas_productos.productos"))


