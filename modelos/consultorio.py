from modelos.base_datos import db 

class Consultorio(db.Model):
    __tablename__ = 'consultorio'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    lugar = db.Column(db.String(255), nullable=False)

    pacientes = db.relationship('Paciente', backref='consultorio', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "lugar": self.lugar
        }