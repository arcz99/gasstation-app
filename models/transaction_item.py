from models import db
from sqlalchemy.orm import relationship

class TransactionItem(db.Model):
    __tablename__ = 'transaction_items'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    pump_id = db.Column(db.Integer, db.ForeignKey('pumps.id'), nullable=True)
    pump = relationship('Pump')

    transaction = relationship('Transaction', backref='items')
    product = relationship('Product')

    def __repr__(self):
        return f'<TransactionItem {self.product.name} x{self.quantity}>'