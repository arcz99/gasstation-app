from models import db
from sqlalchemy.orm import relationship

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # np. "Pending", "Completed"

    item = relationship('InventoryItem', backref='orders')

    def __repr__(self):
        return f'<Order {self.id}, Item: {self.item.name}, Quantity: {self.quantity}>'