from flask import Blueprint, request, jsonify
from modelos.base_datos import db
from modelos.paciente import Paciente

paciente_bp = Blueprint('paciente_bp', __name__)

@paciente_bp.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    try:
        pacientes = Paciente.query.all()
        return jsonify([p.to_dict() for p in pacientes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@paciente_bp.route('/pacientes/<int:id>', methods=['GET'])
def obtener_paciente_por_id(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404
    return jsonify(paciente.to_dict()), 200

@paciente_bp.route('/pacientes', methods=['POST'])
def crear_paciente():
    data = request.get_json()
    if not data or 'nombre' not in data or 'documento' not in data:
        return jsonify({"mensaje": "Faltan datos obligatorios (nombre, documento)"}), 400
    
    try:
        nuevo_paciente = Paciente(
            nombre=data['nombre'],
            documento=data['documento'],
            email=data.get('email'),
            telefono=data.get('telefono'),
            consultorio_id=data.get('consultorio_id') # Puede ser None (Null) según el modelo
        )
        db.session.add(nuevo_paciente)
        db.session.commit()
        return jsonify({"mensaje": "Paciente creado con éxito", "paciente": nuevo_paciente.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al registrar paciente. Asegúrese de que el documento/email sean únicos.", "detalle": str(e)}), 400

@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def actualizar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404
    
    data = request.get_json()
    try:
        if 'nombre' in data:
            paciente.nombre = data['nombre']
        if 'documento' in data:
            paciente.documento = data['documento']
        if 'email' in data:
            paciente.email = data['email']
        if 'telefono' in data:
            paciente.telefono = data['telefono']
        if 'consultorio_id' in data:
            paciente.consultorio_id = data['consultorio_id']
            
        db.session.commit()
        return jsonify({"mensaje": "Paciente actualizado con éxito", "paciente": paciente.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@paciente_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def eliminar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404
    try:
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({"mensaje": f"Paciente con ID {id} eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500