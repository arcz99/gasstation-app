from models import db
from sqlalchemy.orm import relationship

class FuelType(db.Model):
    __tablename__ = 'fuel_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = relationship('Product', backref='fuel_types')

    def __repr__(self):
        return f'<FuelType {self.name}>'