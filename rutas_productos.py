# Importar Blueprint y render_template desde Flask
from flask import Blueprint, render_template

# Crear el Blueprint para agrupar las rutas relacionadas con productos
# El primer argumento es el nombre del blueprint, y __name__ ayuda a ubicar recursos como plantillas
rutas_productos = Blueprint("rutas_productos", __name__)

# ------------------- Rutas de Productos -------------------

@rutas_productos.route("/productos")
def productos():
    """
    Función asociada a la ruta /productos.
    Retorna la plantilla productos.html, donde se mostrará el formulario
    y la lista de productos obtenidos desde la API.
    """
    return render_template("productos.html")
