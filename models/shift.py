from models import db
from sqlalchemy.orm import relationship

class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    employee = relationship('Employee', backref='shifts')

    def __repr__(self):
        return f'<Shift Employee {self.employee_id}: {self.start_time} - {self.end_time}>'