from models import db
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    pump_id = db.Column(db.Integer, db.ForeignKey('pumps.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Europe/Warsaw")))

    employee = relationship('Employee', backref='transactions')
    pump = relationship('Pump', backref='transactions')
    customer = relationship('Customer', backref='transactions')

    payment_method = db.Column(db.String(20), nullable=False, default="cash")  # cash, card, transfer
    payment_deadline = db.Column(db.Date, nullable=True)  # tylko dla przelewów
    bank_account = db.Column(db.String(50), nullable=True)  # tylko dla przelewów
    cash_given = db.Column(db.Float, nullable=True)  # tylko przy gotówce
    change_due = db.Column(db.Float, nullable=True)  # tylko przy gotówce

    def __repr__(self):
        return f'<Transaction {self.id}, Amount: {self.amount}>'