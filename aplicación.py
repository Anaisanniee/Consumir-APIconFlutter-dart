from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# 1. Inicializar la app de Flask
app = Flask(__name__)
app.config.from_object(Config)
app.json.ensure_ascii = False

# 2. Permitir que Flutter se conecte a la API sin bloqueos
CORS(app)

# 3. Una ruta de prueba rápida (Endpoint raíz)
@app.route('/', methods=['GET'])
def inicio():
    return jsonify({
        "mensaje": "¡API en Python funcionando correctamente!",
        "estado": "Listo para conectar con Flutter"
    })

# 4. Encender el servidor
if __name__ == '__main__':
    app.run(port=app.config['PORT'])