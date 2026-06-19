import mimetypes
mimetypes.add_type('application/javascript', '.js')
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint

# Importar la instancia centralizada de la base de datos
from modelos.base_datos import db

from modelos.consultorio import Consultorio
from modelos.medico import Medico
from modelos.paciente import Paciente
from modelos.cita import Cita

# === NUEVAS IMPORTACIONES: Archivos de Rutas ===
# === NUEVAS IMPORTACIONES: Archivos de Rutas ===
from routes.cita_routes import cita_rutas_bp
from routes.consultorio_routes import consultorio_rutas_bp
from routes.medico_routes import medico_rutas_bp
from routes.paciente_routes import paciente_rutas_bp

# Inicializar la app de Flask y cargar configuraciones
app = Flask(__name__)
app.config.from_object(Config)

# Configurar para que respete tildes y eñes en las respuestas JSON
app.json.ensure_ascii = False

# Permitir que tu aplicación de Flutter se conecte sin bloqueos de seguridad
CORS(app)

# Vincular la base de datos con la aplicación de Flask
db.init_app(app)

#Configuracion de swagger

SWAGGER_URL = '/docs'  # URL en el navegador: http://localhost:5000/docs
API_URL = 'http://localhost:5000/swagger.json'  

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Documentación API Médica"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Ruta para que Flask sirva el archivo swagger.json que acabas de llenar
@app.route('/docs')
def swagger_ui():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8" />
        <title>Documentación API Médica</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = () => {
                window.ui = SwaggerUIBundle({
                    url: '/swagger.json',
                    dom_id: '#swagger-ui',
                });
            };
        </script>
    </body>
    </html>
    """

# Ruta para que Flask sirva tu archivo swagger.json local
@app.route('/swagger.json')
def serve_swagger_spec():
    import json
    with open('swagger.json', 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

# === REGISTRO DE BLUEPRINTS (Rutas Limpias) ===
app.register_blueprint(cita_rutas_bp, url_prefix='/api')
app.register_blueprint(consultorio_rutas_bp, url_prefix='/api')
app.register_blueprint(medico_rutas_bp, url_prefix='/api')
app.register_blueprint(paciente_rutas_bp, url_prefix='/api')

# Crear las tablas en Laragon automáticamente (si no existen todavía)
with app.app_context():
    db.create_all()

# Una ruta de prueba rápida (Endpoint raíz)
@app.route('/', methods=['GET'])
def inicio():
    return jsonify({
        "mensaje": "¡API Médica en Python funcionando correctamente!",
        "estado": "Rutas desacopladas de los controladores y base de datos sincronizada con Laragon"
    })

# Encender el servidor
if __name__ == '__main__':
    app.run(port=app.config['PORT'])