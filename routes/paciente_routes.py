from flask import Blueprint
from controladores.paciente_controller import (
    obtener_pacientes, 
    obtener_paciente_por_id, 
    crear_paciente, 
    actualizar_paciente, 
    eliminar_paciente
)

# Creamos el Blueprint exclusivo para las URLs de pacientes
paciente_rutas_bp = Blueprint('paciente_rutas_bp', __name__)

# Mapeo directo de las URLs a las funciones del controlador
paciente_rutas_bp.route('/pacientes', methods=['GET'])(obtener_pacientes)
paciente_rutas_bp.route('/pacientes/<int:id>', methods=['GET'])(obtener_paciente_por_id)
paciente_rutas_bp.route('/pacientes', methods=['POST'])(crear_paciente)
paciente_rutas_bp.route('/pacientes/<int:id>', methods=['PUT'])(actualizar_paciente)
paciente_rutas_bp.route('/pacientes/<int:id>', methods=['DELETE'])(eliminar_paciente)