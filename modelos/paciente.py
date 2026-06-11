from modelos.base_datos import db

class Paciente(db.Model):
    __tablename__ = 'paciente'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    consultorio_id = db.Column(db.Integer, db.ForeignKey('consultorio.id', ondelete='SET NULL'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "documento": self.documento,
            "email": self.email,
            "telefono": self.telefono,
            "consultorio_id": self.consultorio_id
        }