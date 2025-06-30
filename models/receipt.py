from models import db
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from zoneinfo import ZoneInfo

class Receipt(db.Model):
    __tablename__ = 'receipts'
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(30), unique=True, nullable=False)  # NOWE
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False, unique=True)
    date = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Europe/Warsaw")))
    amount = db.Column(db.Float, nullable=False)

    transaction = relationship('Transaction', backref=backref('receipt', uselist=False))

    def __repr__(self):
        return f'<Receipt {self.receipt_number}, Amount: {self.amount}>'