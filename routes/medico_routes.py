from flask import Blueprint
from controladores.medico_controller import (
    obtener_medicos,
    obtener_medico_por_id,
    crear_medico,
    actualizar_medico,
    eliminar_medico
)

# Creamos el Blueprint exclusivo para las URLs de médicos
medico_rutas_bp = Blueprint('medico_rutas_bp', __name__)

# Mapeo directo de las URLs a las funciones del controlador
medico_rutas_bp.route('/medicos', methods=['GET'])(obtener_medicos)
medico_rutas_bp.route('/medicos/<int:id>', methods=['GET'])(obtener_medico_por_id)
medico_rutas_bp.route('/medicos', methods=['POST'])(crear_medico)
medico_rutas_bp.route('/medicos/<int:id>', methods=['PUT'])(actualizar_medico)
medico_rutas_bp.route('/medicos/<int:id>', methods=['DELETE'])(eliminar_medico)