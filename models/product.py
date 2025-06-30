from models import db
from sqlalchemy.orm import relationship
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_type = db.Column(db.String(20), nullable=False)  # 'fuel', 'oil', 'other'
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    category = relationship('ProductCategory')
    stock = db.Column(db.Float, nullable=False, default=0.0)  # Stan magazynowy

    def __repr__(self):
        return f'<Product {self.name} ({self.product_type})>'