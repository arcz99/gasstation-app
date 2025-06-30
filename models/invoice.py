from models import db
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from zoneinfo import ZoneInfo
class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    invoice_number = db.Column(db.String(30), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Europe/Warsaw")))
    amount = db.Column(db.Float, nullable=False)

    # Poprawiony backref!
    transaction = relationship('Transaction', backref=backref('invoice', uselist=False))
    customer = relationship('Customer', backref='invoices')

    def __repr__(self):
        return f'<Invoice {self.invoice_number}, Customer: {self.customer_id}>'