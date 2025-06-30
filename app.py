from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from models import db, Employee, FuelType, User, Pump, Transaction, Customer, Receipt, Invoice, TransactionItem, \
    Product, ProductCategory
from zoneinfo import ZoneInfo
from datetime import datetime, date
from sqlalchemy import or_
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gas_station.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/employees')
@login_required
def employee_list():
    if current_user.role != 'manager':
        abort(403)
    employees = Employee.query.all()
    return render_template('employee_list.html', employees=employees)

@app.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if current_user.role != 'manager':
        abort(403)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        new_employee = Employee(first_name=first_name, last_name=last_name, position=position, user_id=user.id)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('employee_list'))
    return render_template('add_employee.html')

@app.route('/fueltypes')
@login_required
def fueltype_list():
    if current_user.role != 'manager':
        abort(403)
    fueltypes = FuelType.query.all()
    return render_template('fueltype_list.html', fueltypes=fueltypes)

@app.route('/fueltypes/add', methods=['GET', 'POST'])
@login_required
def add_fueltype():
    if current_user.role != 'manager':
        abort(403)
    error = None
    fuel_products = Product.query.filter_by(product_type="fuel").all()
    if request.method == 'POST':
        name = request.form['name']
        product_id = int(request.form['product_id'])
        if FuelType.query.filter_by(name=name).first():
            error = "Fuel type with this name already exists!"
        else:
            fueltype = FuelType(name=name, product_id=product_id)
            db.session.add(fueltype)
            db.session.commit()
            return redirect(url_for('fueltype_list'))
    return render_template('add_fueltype.html', fuel_products=fuel_products, error=error)
@app.route('/fueltypes/edit/<int:fueltype_id>', methods=['GET', 'POST'])
@login_required
def edit_fueltype(fueltype_id):
    if current_user.role != 'manager':
        abort(403)
    fueltype = FuelType.query.get_or_404(fueltype_id)
    if request.method == 'POST':
        name = request.form['name']
        # sprawdzenie duplikatów
        if FuelType.query.filter_by(name=name).first() and name != fueltype.name:
            return "This fuel type already exists!", 400
        fueltype.name = name
        db.session.commit()
        return redirect(url_for('fueltype_list'))
    return render_template('edit_fueltype.html', fueltype=fueltype)

@app.route('/fueltypes/delete/<int:fueltype_id>', methods=['POST'])
@login_required
def delete_fueltype(fueltype_id):
    if current_user.role != 'manager':
        abort(403)
    fueltype = FuelType.query.get_or_404(fueltype_id)
    db.session.delete(fueltype)
    db.session.commit()
    return redirect(url_for('fueltype_list'))
@app.route('/pumps')
@login_required
def pump_list():
    if current_user.role != 'manager':
        abort(403)
    pumps = Pump.query.all()
    return render_template('pump_list.html', pumps=pumps)
@app.route('/pumps/add', methods=['GET', 'POST'])
@login_required
def add_pump():
    if current_user.role != 'manager':
        abort(403)
    fueltypes = FuelType.query.all()
    if request.method == 'POST':
        pump_number = request.form['pump_number']
        fuel_type_id = request.form['fuel_type_id']
        if Pump.query.filter_by(pump_number=pump_number).first():
            return "This pump number already exists!", 400
        new_pump = Pump(pump_number=pump_number, fuel_type_id=fuel_type_id)
        db.session.add(new_pump)
        db.session.commit()
        return redirect(url_for('pump_list'))
    return render_template('add_edit_pump.html', pump=None, fueltypes=fueltypes)
@app.route('/pumps/edit/<int:pump_id>', methods=['GET', 'POST'])
@login_required
def edit_pump(pump_id):
    if current_user.role != 'manager':
        abort(403)
    pump = Pump.query.get_or_404(pump_id)
    fueltypes = FuelType.query.all()
    if request.method == 'POST':
        pump_number = request.form['pump_number']
        fuel_type_id = request.form['fuel_type_id']
        # sprawdzenie duplikatów
        if Pump.query.filter(Pump.pump_number == pump_number, Pump.id != pump.id).first():
            return "This pump number already exists!", 400
        pump.pump_number = pump_number
        pump.fuel_type_id = fuel_type_id
        db.session.commit()
        return redirect(url_for('pump_list'))
    return render_template('add_edit_pump.html', pump=pump, fueltypes=fueltypes)
@app.route('/pumps/delete/<int:pump_id>', methods=['POST'])
@login_required
def delete_pump(pump_id):
    if current_user.role != 'manager':
        abort(403)
    pump = Pump.query.get_or_404(pump_id)
    db.session.delete(pump)
    db.session.commit()
    return redirect(url_for('pump_list'))
@app.route('/transactions')
@login_required
def transaction_list():
    if current_user.role not in ['manager', 'worker']:
        return render_template('transaction_list.html', transactions=[])

    doc_type = request.args.get('doc_type')
    q = request.args.get('q', '').strip()

    transactions = Transaction.query

    # Filtrowanie po typie dokumentu
    if doc_type == 'receipt':
        transactions = transactions.join(Transaction.receipt).filter(Transaction.receipt != None)
    elif doc_type == 'invoice':
        transactions = transactions.join(Transaction.invoice).filter(Transaction.invoice != None)

    # Wyszukiwarka
    if q:
        transactions = transactions.outerjoin(Transaction.invoice).outerjoin(Transaction.customer)
        transactions = transactions.filter(
            or_(
                Transaction.amount.like(f'%{q}%'),
                Invoice.invoice_number.like(f'%{q}%'),
                Customer.company_name.like(f'%{q}%'),
                Customer.first_name.like(f'%{q}%'),
                Customer.last_name.like(f'%{q}%')
            )
        )

    transactions = transactions.order_by(Transaction.date.desc()).all()
    return render_template('transaction_list.html', transactions=transactions)

@app.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if current_user.role not in ['manager', 'worker']:
        abort(403)
    pumps = Pump.query.all()
    customers = Customer.query.all()

    if request.method == 'POST':
        pump_id = request.form['pump_id']
        litres = float(request.form['litres'])
        amount = float(request.form['amount'])
        customer_id = request.form.get('customer_id') or None  # None = paragon

        pump = Pump.query.get(pump_id)
        product = pump.fuel_type.product if pump and pump.fuel_type else None

        if product:
            if product.stock < litres:
                error = f"Not enough stock for {product.name} (available: {product.stock}, needed: {litres})"
                return render_template('add_transaction.html', pumps=pumps, customers=customers, error=error)
        else:
            error = "Invalid pump or fuel type!"
            return render_template('add_transaction.html', pumps=pumps, customers=customers, error=error)

        employee = Employee.query.filter_by(user_id=current_user.id).first()
        if not employee:
            return "No matching employee for current user!", 400

        transaction = Transaction(
            employee_id=employee.id,
            pump_id=pump_id,
            customer_id=customer_id,
            amount=amount
        )
        db.session.add(transaction)
        db.session.commit()

        # ODEJMIJ ilość z magazynu
        if product:
            product.stock -= litres


        if customer_id:  # faktura
            invoice_number = f"FV{transaction.id:05d}/{datetime.now().year}"
            invoice = Invoice(
                transaction_id=transaction.id,
                customer_id=customer_id,
                invoice_number=invoice_number,
                amount=amount
            )
            db.session.add(invoice)
        else:  # paragon
            receipt_number = f"RCPT{transaction.id:05d}/{datetime.now().year}"
            receipt = Receipt(
                transaction_id=transaction.id,
                receipt_number=receipt_number,
                amount=amount
            )
            db.session.add(receipt)

        db.session.commit()
        return redirect(url_for('transaction_list'))

    # GET
    return render_template('add_transaction.html', pumps=pumps, customers=customers)
@app.route('/customers')
@login_required
def customer_list():
    if current_user.role not in ['manager', 'worker']:
        abort(403)
    customers = Customer.query.all()
    return render_template('customer_list.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if current_user.role not in ['manager', 'worker']:
        abort(403)
    if request.method == 'POST':
        customer_type = request.form['customer_type']
        address = request.form['address']
        email = request.form.get('email')
        if customer_type == 'company':
            company_name = request.form['company_name']
            nip = request.form['nip']
            customer = Customer(
                customer_type='company',
                company_name=company_name,
                nip=nip,
                address=address,
                email=email
            )
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            customer = Customer(
                customer_type='individual',
                first_name=first_name,
                last_name=last_name,
                address=address,
                email=email
            )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customer_list'))

    return render_template('add_customer.html')

@app.route('/receipts/<int:receipt_id>')
@login_required
def view_receipt(receipt_id):
    receipt = Receipt.query.get_or_404(receipt_id)
    return render_template('receipt.html', receipt=receipt)

@app.route('/invoices/<int:invoice_id>')
@login_required
def view_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('invoice.html', invoice=invoice)

@app.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    pumps = Pump.query.all()
    fuels = FuelType.query.all()
    products = Product.query.filter(Product.product_type != "fuel").all()
    customers = Customer.query.all()

    if request.method == 'POST':
        import json

        cart = json.loads(request.form['cart_data'])
        payment_method = request.form['payment_method']
        checkout_type = request.form['checkout_type']  # 'receipt' lub 'invoice'
#sprawdzanie stanu magazynu
        insufficient_stock = []
        for item in cart:
            product = Product.query.get(item['productId'])
            qty_needed = float(item['qty'])
            if product and product.stock < qty_needed:
                insufficient_stock.append(f"{product.name} (available: {product.stock}, needed: {qty_needed})")

        if insufficient_stock:
            error_message = "Not enough stock for: " + ", ".join(insufficient_stock)
            pumps = Pump.query.all()
            fuels = FuelType.query.all()
            products = Product.query.filter(Product.product_type != "fuel").all()
            customers = Customer.query.all()
            return render_template(
                'sales.html',
                pumps=pumps, fuels=fuels, products=products, customers=customers,
                error=error_message
            )
        # Sprawdź, czy koszyk nie jest pusty
        if not cart:
            return "Cart is empty!", 400

        # Zbierz sumę transakcji
        total = sum(item['price'] * float(item['qty']) for item in cart)

        # Pobierz pracownika z user_id
        employee = Employee.query.filter_by(user_id=current_user.id).first()
        if not employee:
            return "Employee not found!", 400

        # Ustal klienta
        customer_id = None
        if checkout_type == "invoice":
            customer_id = request.form.get('customer_id')
            if not customer_id:
                return "No customer selected for invoice!", 400

        # Utwórz Transaction
        transaction = Transaction(
            employee_id=employee.id,
            pump_id=None,
            customer_id=customer_id,
            amount=total,
            date=datetime.now(),
            payment_method=payment_method
        )

        # Obsługa pól płatności:
        if payment_method == 'cash':
            cash_given = float(request.form.get('cash_given', '0') or 0)
            transaction.cash_given = cash_given
            transaction.change_due = cash_given - total if cash_given >= total else 0
        elif payment_method == 'transfer':
            transaction.payment_deadline = request.form.get('payment_deadline')
            transaction.bank_account = request.form.get('bank_account')

        db.session.add(transaction)
        db.session.commit()

        # Dodaj wszystkie pozycje z koszyka
        for item in cart:
            transaction_item = TransactionItem(
                transaction_id=transaction.id,
                product_id=item['productId'],
                quantity=float(item['qty']),
                price=float(item['price']),
                total=float(item['qty']) * float(item['price'])
            )
            db.session.add(transaction_item)
            product = Product.query.get(item['productId'])
            if product:
                product.stock -= float(item['qty'])
        db.session.commit()

        # Paragon czy faktura?
        if checkout_type == 'receipt':
            from zoneinfo import ZoneInfo
            receipt_number = f"RCPT{transaction.id:05d}/{date.today().year}"
            receipt = Receipt(
                transaction_id=transaction.id,
                receipt_number=receipt_number,
                amount=total,
                date=datetime.now(ZoneInfo("Europe/Warsaw"))
            )
            db.session.add(receipt)
            db.session.commit()
            return redirect(url_for('view_receipt', receipt_id=receipt.id))

        elif checkout_type == 'invoice':
            from zoneinfo import ZoneInfo
            invoice_number = f"FV{transaction.id:05d}/{date.today().year}"
            invoice = Invoice(
                transaction_id=transaction.id,
                customer_id=customer_id,
                invoice_number=invoice_number,
                amount=total,
                date=datetime.now(ZoneInfo("Europe/Warsaw"))
            )
            db.session.add(invoice)
            db.session.commit()
            return redirect(url_for('view_invoice', invoice_id=invoice.id))

        else:
            return "Unknown checkout type!", 400

    # GET – renderuj stronę sprzedaży
    return render_template('sales.html', pumps=pumps, fuels=fuels, products=products, customers=customers)
@app.route('/products')
@login_required
def product_list():
    if current_user.role != 'manager':
        abort(403)
    products = Product.query.all()
    return render_template('product_list.html', products=products)

# Dodawanie produktu
@app.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'manager':
        abort(403)
    error = None
    categories = ProductCategory.query.all()
    if request.method == 'POST':
        name = request.form['name']
        stock = float(request.form['stock'])
        price = float(request.form['price'])
        product_type = request.form['product_type']
        category_id = int(request.form['category_id'])

        if Product.query.filter_by(name=name).first():
            error = "Product with this name already exists!"
        else:
            product = Product(
                name=name,
                price=price,
                product_type=product_type,
                category_id=category_id,
                stock = stock
            )
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('product_list'))

    return render_template('add_product.html', categories=categories, error=error)

# Edycja produktu
@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if current_user.role != 'manager':
        abort(403)
    product = Product.query.get_or_404(product_id)
    error = None
    categories = ProductCategory.query.all()
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = float(request.form['stock'])
        product_type = request.form['product_type']
        category_id = int(request.form['category_id'])

        if Product.query.filter(Product.id != product.id, Product.name == name).first():
            error = "Another product with this name already exists!"
        else:
            product.name = name
            product.price = price
            product.product_type = product_type
            product.category_id = category_id
            product.stock = stock
            db.session.commit()
            return redirect(url_for('product_list'))
    return render_template('edit_product.html', product=product, categories=categories, error=error)
# Usuwanie produktu
@app.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if current_user.role != 'manager':
        abort(403)
    product = Product.query.get_or_404(product_id)
    if product.fuel_types:  # sprawdza powiązane FuelType
        return "Cannot delete product: it is assigned to at least one FuelType.", 400
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product_list'))
@app.route('/products/search')
@login_required
def search_products():
    query = request.args.get('q', '').strip()
    products = []
    if query:
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    result = [
        {
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'product_type': p.product_type,
            'vat_rate': p.category.vat_rate if p.category else 0
        }
        for p in products
    ]
    return jsonify(result)


# LISTA kategorii
@app.route('/categories')
@login_required
def category_list():
    if current_user.role != 'manager':
        abort(403)
    categories = ProductCategory.query.all()
    return render_template('category_list.html', categories=categories)

# DODAWANIE kategorii
@app.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.role != 'manager':
        abort(403)
    error = None
    if request.method == 'POST':
        name = request.form['name']
        vat_rate = float(request.form['vat_rate'])
        if ProductCategory.query.filter_by(name=name).first():
            error = "Category with this name already exists!"
        else:
            category = ProductCategory(name=name, vat_rate=vat_rate)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('category_list'))
    return render_template('add_category.html', error=error)

# EDYCJA kategorii
@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if current_user.role != 'manager':
        abort(403)
    category = ProductCategory.query.get_or_404(category_id)
    error = None
    if request.method == 'POST':
        name = request.form['name']
        vat_rate = float(request.form['vat_rate'])
        if ProductCategory.query.filter(ProductCategory.id != category.id, ProductCategory.name == name).first():
            error = "Another category with this name already exists!"
        else:
            category.name = name
            category.vat_rate = vat_rate
            db.session.commit()
            return redirect(url_for('category_list'))
    return render_template('edit_category.html', category=category, error=error)

# USUWANIE kategorii
@app.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if current_user.role != 'manager':
        abort(403)
    category = ProductCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('category_list'))

@app.route('/stock')
@login_required
def stock_list():
    if current_user.role != 'manager':
        abort(403)
    products = Product.query.all()
    return render_template('stock_list.html', products=products)
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    error = None
    success = None
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if not current_user.check_password(old_password):
            error = "Incorrect old password!"
        elif len(new_password) < 6:
            error = "New password too short!"
        else:
            current_user.set_password(new_password)
            db.session.commit()
            success = "Password changed successfully."
    return render_template('change_password.html', error=error, success=success)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')