from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Importar la instancia centralizada de la base de datos
from modelos.base_datos import db

from modelos.consultorio import Consultorio
from modelos.medico import Medico
from modelos.paciente import Paciente
from modelos.cita import Cita

# Inicializar la app de Flask y cargar configuraciones
app = Flask(__name__)
app.config.from_object(Config)

# Configurar para que respete tildes y eñes en las respuestas JSON
app.json.ensure_ascii = False

# Permitir que tu aplicación de Flutter se conecte sin bloqueos de seguridad
CORS(app)

# Vincular la base de datos con la aplicación de Flask
db.init_app(app)

# Crear las tablas en Laragon automáticamente (si no existen todavía)
with app.app_context():
    db.create_all()

# Una ruta de prueba rápida (Endpoint raíz)
@app.route('/', methods=['GET'])
def inicio():
    return jsonify({
        "mensaje": "¡API Médica en Python funcionando correctamente!",
        "estado": "Modelos cargados y base de datos sincronizada con Laragon"
    })

# encender el servidor
if __name__ == '__main__':
    app.run(port=app.config['PORT'])