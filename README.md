# Proyecto Flask con Jinja2

Este proyecto implementa un frontend en **Flask** utilizando el motor de plantillas **Jinja2**, con el objetivo de conectarse a una API que gestiona productos, facturas, clientes y vendedores. La aplicación se organiza con **Blueprints** para mantener un código modular y fácil de mantener.

---

## Estructura del proyecto

- **app.py**: archivo principal de la aplicación Flask. Crea la instancia de la app y registra los Blueprints.  
- **rutas_productos.py**: Blueprint con las rutas de la sección de productos.  
- **templates/**: plantillas HTML del proyecto.  
  - `base.html` (plantilla base con encabezado, menú y pie de página)  
  - `index.html` (inicio)  
  - `acerca.html` (información del proyecto)  
  - `productos.html` (página de productos) 
  - `clientes.html` (página de clientes)
- **static/**: archivos estáticos, por ejemplo `estilos.css`.  
- **requirements.txt**: dependencias exactas del proyecto.  

---

## Requisitos

- Python 3.11 o superior  
- Git instalado  
- Windows PowerShell o terminal equivalente  

---

## Instalación

1. Clonar el repositorio:
   git clone https://github.com/ccastro2050/frontflask_jinja.git
   cd frontflask_jinja

2. Crear y activar el entorno virtual:
python -m venv .venv
.\.venv\Scripts\activate

3. Instalar dependencias:
pip install -r requirements.txt

4. Ejecución

Iniciar el servidor de desarrollo:
python app.py


