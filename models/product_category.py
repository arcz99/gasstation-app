from models import db

class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    vat_rate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<ProductCategory {self.name} ({self.vat_rate}%)>'