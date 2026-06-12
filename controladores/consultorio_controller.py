from flask import Blueprint, request, jsonify
from modelos.base_datos import db
from modelos.consultorio import Consultorio

consultorio_bp = Blueprint('consultorio_bp', __name__)

@consultorio_bp.route('/consultorios', methods=['GET'])
def obtener_consultorios():
    try:
        consultorios = Consultorio.query.all()
        return jsonify([c.to_dict() for c in consultorios]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@consultorio_bp.route('/consultorios/<int:id>', methods=['GET'])
def obtener_consultorio_por_id(id):
    consultorio = Consultorio.query.get(id)
    if not consultorio:
        return jsonify({"mensaje": "Consultorio no encontrado"}), 404
    return jsonify(consultorio.to_dict()), 200

@consultorio_bp.route('/consultorios', methods=['POST'])
def crear_consultorio():
    data = request.get_json()
    if not data or 'nombre' not in data or 'lugar' not in data:
        return jsonify({"mensaje": "Faltan datos obligatorios (nombre, lugar)"}), 400
    
    try:
        nuevo_consultorio = Consultorio(
            nombre=data['nombre'],
            lugar=data['lugar']
        )
        db.session.add(nuevo_consultorio)
        db.session.commit()
        return jsonify({"mensaje": "Consultorio creado con éxito", "consultorio": nuevo_consultorio.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@consultorio_bp.route('/consultorios/<int:id>', methods=['PUT'])
def actualizar_consultorio(id):
    consultorio = Consultorio.query.get(id)
    if not consultorio:
        return jsonify({"mensaje": "Consultorio no encontrado"}), 404
    
    data = request.get_json()
    try:
        if 'nombre' in data:
            consultorio.nombre = data['nombre']
        if 'lugar' in data:
            consultorio.lugar = data['lugar']
            
        db.session.commit()
        return jsonify({"mensaje": "Consultorio actualizado con éxito", "consultorio": consultorio.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@consultorio_bp.route('/consultorios/<int:id>', methods=['DELETE'])
def eliminar_consultorio(id):
    consultorio = Consultorio.query.get(id)
    if not consultorio:
        return jsonify({"mensaje": "Consultorio no encontrado"}), 404
    try:
        db.session.delete(consultorio)
        db.session.commit()
        return jsonify({"mensaje": f"Consultorio con ID {id} eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500