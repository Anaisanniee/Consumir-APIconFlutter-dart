from modelos.consultorio import db

class Cita(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id', ondelete='CASCADE'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')

    # Relaciones para acceder fácilmente a la información del médico o paciente desde la cita
    paciente = db.relationship('Paciente', backref='citas', lazy=True)
    medico = db.relationship('Medico', backref='citas', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "paciente_id": self.paciente_id,
            "medico_id": self.medico_id,
            "fecha": self.fecha.strftime('%Y-%m-%d') if self.fecha else None,
            "hora": self.hora.strftime('%H:%M:%S') if self.hora else None,
            "estado": self.estado
        }