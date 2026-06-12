from flask import Blueprint, request, jsonify
from modelos.base_datos import db
from modelos.cita import Cita
from datetime import datetime

# Creamos el Blueprint para las rutas de citas
cita_bp = Blueprint('cita_bp', __name__)

# 1. OBTENER TODAS LAS CITAS (GET)
@cita_bp.route('/citas', methods=['GET'])
def obtener_citas():
    try:
        citas = Cita.query.all()
        return jsonify([cita.to_dict() for cita in citas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2. OBTENER UNA CITA POR ID (GET)
@cita_bp.route('/citas/<int:id>', methods=['GET'])
def obtener_cita_por_id(id):
    cita = Cita.query.get(id)
    if not cita:
        return jsonify({"mensaje": "Cita no encontrada"}), 404
    return jsonify(cita.to_dict()), 200


# 3. CREAR UNA NUEVA CITA (POST)
@cita_bp.route('/citas', methods=['POST'])
def crear_cita():
    data = request.get_json()
    
    # Validar campos obligatorios
    if not data or 'paciente_id' not in data or 'medico_id' not in data or 'fecha' not in data or 'hora' not in data:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400
    
    try:
        # Convertir cadenas de texto a objetos date y time de Python
        fecha_obj = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        hora_obj = datetime.strptime(data['hora'], '%H:%M:%S').time()

        nueva_cita = Cita(
            paciente_id=data['paciente_id'],
            medico_id=data['medico_id'],
            fecha=fecha_obj,
            hora=hora_obj,
            estado=data.get('estado', 'Pendiente') # Si no mandan estado, se pone 'Pendiente'
        )

        db.session.add(nueva_cita)
        db.session.commit()

        return jsonify({"mensaje": "Cita creada con éxito", "cita": nueva_cita.to_dict()}), 201

    except ValueError:
        return jsonify({"mensaje": "Formato de fecha (%Y-%m-%d) o hora (%H:%M:%S) inválido"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# 4. ACTUALIZAR UNA CITA (PUT)
@cita_bp.route('/citas/<int:id>', methods=['PUT'])
def actualizar_cita(id):
    cita = Cita.query.get(id)
    if not cita:
        return jsonify({"mensaje": "Cita no encontrada"}), 404
    
    data = request.get_json()
    
    try:
        if 'paciente_id' in data:
            cita.paciente_id = data['paciente_id']
        if 'medico_id' in data:
            cita.medico_id = data['medico_id']
        if 'estado' in data:
            cita.estado = data['estado']
        if 'fecha' in data:
            cita.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
        if 'hora' in data:
            cita.hora = datetime.strptime(data['hora'], '%H:%M:%S').time()

        db.session.commit()
        return jsonify({"mensaje": "Cita actualizada con éxito", "cita": cita.to_dict()}), 200

    except ValueError:
        return jsonify({"mensaje": "Formato de fecha u hora inválido"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# 5. ELIMINAR UNA CITA (DELETE)
@cita_bp.route('/citas/<int:id>', methods=['DELETE'])
def eliminar_cita(id):
    cita = Cita.query.get(id)
    if not cita:
        return jsonify({"mensaje": "Cita no encontrada"}), 404
    
    try:
        db.session.delete(cita)
        db.session.commit()
        return jsonify({"mensaje": f"Cita con ID {id} eliminada correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500