# Importar la clase principal de Flask y la función para renderizar plantillas
from flask import Flask, render_template

# Crear la instancia de la aplicación Flask
aplicacion = Flask(__name__)

# ------------------- Rutas principales -------------------

@aplicacion.route("/")
def inicio():
    """
    Función asociada a la ruta principal (/).
    Retorna la plantilla index.html.
    """
    return render_template("index.html")


@aplicacion.route("/acerca")
def acerca():
    """
    Función asociada a la ruta /acerca.
    Retorna la plantilla acerca.html con información sobre el proyecto.
    """
    return render_template("acerca.html")


@aplicacion.route("/productos")
def productos():
    """
    Función asociada a la ruta /productos.
    Retorna la plantilla productos.html que mostrará el formulario y la lista de productos.
    """
    return render_template("productos.html")

# ---------------------------------------------------------

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Ejecutar la aplicación en modo depuración, en el puerto 5000
    # host="0.0.0.0" permite acceso desde la red local
    # debug=True permite reinicio automático ante cambios
    aplicacion.run(host="0.0.0.0", port=5000, debug=True)
