from models import db
from sqlalchemy.orm import relationship

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    user = relationship('User', backref='employee', uselist=False)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'