from flask import Blueprint
from controladores.consultorio_controller import (
    obtener_consultorios,
    obtener_consultorio_por_id,
    crear_consultorio,
    actualizar_consultorio,
    eliminar_consultorio
)

# Creamos el Blueprint exclusivo para las URLs de consultorios
consultorio_rutas_bp = Blueprint('consultorio_rutas_bp', __name__)

# Mapeo directo de las URLs a las funciones del controlador
consultorio_rutas_bp.route('/consultorios', methods=['GET'])(obtener_consultorios)
consultorio_rutas_bp.route('/consultorios/<int:id>', methods=['GET'])(obtener_consultorio_por_id)
consultorio_rutas_bp.route('/consultorios', methods=['POST'])(crear_consultorio)
consultorio_rutas_bp.route('/consultorios/<int:id>', methods=['PUT'])(actualizar_consultorio)
consultorio_rutas_bp.route('/consultorios/<int:id>', methods=['DELETE'])(eliminar_consultorio)