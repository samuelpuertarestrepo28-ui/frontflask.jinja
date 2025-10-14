# Importar la clase principal de Flask y la función para renderizar plantillas
from flask import Flask, render_template

# Importar el Blueprint que contiene las rutas de productos
from rutas_productos import rutas_productos
from rutas_clientes import rutas_clientes
from rutas_facturas import rutas_facturas
from rutas_facturas import rutas_vendedores


# Crear la instancia de la aplicación Flask
aplicacion = Flask(__name__)

# ------------------- Registro de Blueprints -------------------
# Registrar el Blueprint de productos en la aplicación principal
aplicacion.register_blueprint(rutas_productos)
aplicacion.register_blueprint(rutas_clientes)
aplicacion.register_blueprint(rutas_facturas)
aplicacion.register_blueprint(rutas_vendedores)

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

# ---------------------------------------------------------

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Ejecutar la aplicación en modo depuración, en el puerto 5000
    # host="0.0.0.0" permite que la app sea accesible desde la red local
    # debug=True permite reinicio automático ante cambios
    aplicacion.run(host="0.0.0.0", port=5000, debug=True)

