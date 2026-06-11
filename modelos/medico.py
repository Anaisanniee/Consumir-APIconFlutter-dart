from modelos.consultorio import db

class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    licencia = db.Column(db.String(50), unique=True, nullable=False)
    disponibilidad_horario = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especialidad": self.especialidad,
            "licencia": self.licencia,
            "disponibilidad_horario": self.disponibilidad_horario
        }