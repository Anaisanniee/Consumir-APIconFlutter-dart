from flask import Blueprint, request, jsonify
from modelos.base_datos import db
from modelos.medico import Medico

medico_bp = Blueprint('medico_bp', __name__)

@medico_bp.route('/medicos', methods=['GET'])
def obtener_medicos():
    try:
        medicos = Medico.query.all()
        return jsonify([m.to_dict() for m in medicos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@medico_bp.route('/medicos/<int:id>', methods=['GET'])
def obtener_medico_por_id(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({"mensaje": "Médico no encontrado"}), 404
    return jsonify(medico.to_dict()), 200

@medico_bp.route('/medicos', methods=['POST'])
def crear_medico():
    data = request.get_json()
    if not data or 'nombre' not in data or 'especialidad' not in data or 'licencia' not in data:
        return jsonify({"mensaje": "Faltan datos obligatorios (nombre, especialidad, licencia)"}), 400
    
    try:
        nuevo_medico = Medico(
            nombre=data['nombre'],
            especialidad=data['especialidad'],
            licencia=data['licencia'],
            disponibilidad_horario=data.get('disponibilidad_horario')
        )
        db.session.add(nuevo_medico)
        db.session.commit()
        return jsonify({"mensaje": "Médico creado con éxito", "medico": nuevo_medico.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        # Manejo por si la licencia (que es unique) ya existe
        return jsonify({"error": "Error al guardar el médico. Verifique que la licencia sea única.", "detalle": str(e)}), 400

@medico_bp.route('/medicos/<int:id>', methods=['PUT'])
def actualizar_medico(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({"mensaje": "Médico no encontrado"}), 404
    
    data = request.get_json()
    try:
        if 'nombre' in data:
            medico.nombre = data['nombre']
        if 'especialidad' in data:
            medico.especialidad = data['especialidad']
        if 'licencia' in data:
            medico.licencia = data['licencia']
        if 'disponibilidad_horario' in data:
            medico.disponibilidad_horario = data['disponibilidad_horario']
            
        db.session.commit()
        return jsonify({"mensaje": "Médico actualizado con éxito", "medico": medico.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@medico_bp.route('/medicos/<int:id>', methods=['DELETE'])
def eliminar_medico(id):
    medico = Medico.query.get(id)
    if not medico:
        return jsonify({"mensaje": "Médico no encontrado"}), 404
    try:
        db.session.delete(medico)
        db.session.commit()
        return jsonify({"mensaje": f"Médico con ID {id} eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500