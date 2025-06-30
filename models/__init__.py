from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .employee import Employee
from .fuel_type import FuelType
from .pump import Pump
from .customer import Customer
from .transaction import Transaction
from .inventory_item import InventoryItem
from .order import Order
from .shift import Shift
from .promotion import Promotion
from .receipt import Receipt
from .invoice import Invoice
from .user import User
from .product import Product
from .transaction_item import TransactionItem
from .product_category import ProductCategory