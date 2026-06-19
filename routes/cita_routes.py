from flask import Blueprint
from controladores.cita_controller import (
    obtener_citas,
    obtener_cita_por_id,
    crear_cita,
    actualizar_cita,
    eliminar_cita
)

# Creamos el Blueprint exclusivo para las URLs de citas
cita_rutas_bp = Blueprint('cita_rutas_bp', __name__)

# Mapeo directo de las URLs a las funciones del controlador
cita_rutas_bp.route('/citas', methods=['GET'])(obtener_citas)
cita_rutas_bp.route('/citas/<int:id>', methods=['GET'])(obtener_cita_por_id)
cita_rutas_bp.route('/citas', methods=['POST'])(crear_cita)
cita_rutas_bp.route('/citas/<int:id>', methods=['PUT'])(actualizar_cita)
cita_rutas_bp.route('/citas/<int:id>', methods=['DELETE'])(eliminar_cita)