from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# Werkzeug 提供的安全模块。
# 它可以自动为密码生成不可逆的哈希值，避免数据库泄露时明文密码暴露。

# 这个类不是数据本身，而是一种“模板”或“表结构定义”。
class Guest(db.Model):          # 创建一个代表数据库表的 Python 类， 一个名为 Guest 的数据库模型（表），它继承自 SQLAlchemy 的 Model 类
    __tablename__ = 'guests'    # 指定数据库中表的名字为 “guests”

    # db.Column(...) 定义表中的每一列（字段）
    # 在数据库里，我们叫它 字段 (field or column)，
    # Guest的每个属性 对应（映射） 表中的一列（column）
    # eg. The Guest model has an attribute named email, which maps to the email column in the guests table.
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to reservations
    reservations = db.relationship('Reservation', backref='guest', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # to_dict() 把数据库模型对象转换成干净、可序列化的 Python 字典，方便 Flask jsonify() 输出给前端 在 app.py 。
    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
            'createdAt': self.created_at.isoformat()
        }


class RoomType(db.Model):
    __tablename__ = 'room_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., "Single", "Double", "Suite"
    description = db.Column(db.Text, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    max_occupancy = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.String(255), nullable=False)  # JSON string or comma-separated

    # Relationship to reservations
    reservations = db.relationship('Reservation', backref='room_type', lazy=True)

    def to_dict(self):
        return {
            'roomTypeId': self.id,
            'name': self.name,
            'description': self.description,
            'pricePerNight': self.price_per_night,
            'maxOccupancy': self.max_occupancy,
            'amenities': self.amenities.split(',') if self.amenities else []
        }


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_types.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    number_of_guests = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Confirmed')  # Confirmed, Cancelled, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'reservationId': self.id,
            'roomType': self.room_type.name,
            'totalPrice': self.total_price,
            'checkInDate': self.check_in_date.isoformat(),
            'checkOutDate': self.check_out_date.isoformat(),
            'numberOfGuests': self.number_of_guests,
            'status': self.status,
            'createdAt': self.created_at.isoformat()
        }