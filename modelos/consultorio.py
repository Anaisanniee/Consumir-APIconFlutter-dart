from flask_sqlalchemy import SQLAlchemy

# Inicializamos la instancia de SQLAlchemy que compartiremos
db = SQLAlchemy()

class Consultorio(db.Model):
    __tablename__ = 'consultorio'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    lugar = db.Column(db.String(255), nullable=False)

    # Relación inversa (opcional, ayuda a traer los pacientes de este consultorio)
    pacientes = db.relationship('Paciente', backref='consultorio', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "lugar": self.lugar
        }