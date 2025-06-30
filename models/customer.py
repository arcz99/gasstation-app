from models import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customer_type = db.Column(db.String(20), nullable=False)  # 'company' or 'individual'
    company_name = db.Column(db.String(100))
    nip = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(150))
    email = db.Column(db.String(100))

    def __repr__(self):
        if self.customer_type == "company":
            return f'<Customer (Company) {self.company_name}>'
        else:
            return f'<Customer (Individual) {self.first_name} {self.last_name}>'