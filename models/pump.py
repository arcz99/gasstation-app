from models import db
from sqlalchemy.orm import relationship

class Pump(db.Model):
    __tablename__ = 'pumps'

    id = db.Column(db.Integer, primary_key=True)
    pump_number = db.Column(db.Integer, nullable=False, unique=True)
    fuel_type_id = db.Column(db.Integer, db.ForeignKey('fuel_types.id'), nullable=False)

    # relacja: każda pompa ma jeden rodzaj paliwa, każdy rodzaj paliwa może być w wielu pompach
    fuel_type = relationship('FuelType', backref='pumps')

    def __repr__(self):
        return f'<Pump {self.pump_number} ({self.fuel_type.name})>'