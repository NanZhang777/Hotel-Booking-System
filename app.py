from flask import Flask, request, jsonify
from datetime import datetime, date
from sqlalchemy import and_, or_, not_
from database import db
from models import Guest, RoomType, Reservation

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# 启用 CORS
# 允许 Vite 开发服务器跨域访问 /api/* 接口，并暴露 Authorization 头
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:5173","http://127.0.0.1:5173"]
    }
}, expose_headers=["Authorization"])

# 把 Flask 应用 app 和 SQLAlchemy 数据库对象 db 进行绑定。
# 让 db 知道当前要连接哪个数据库（从 Config 中读取配置）SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hotel.db'
db.init_app(app)

# 创建一个 JWTManager 类型的对象，并传入 Flask 应用对象 app 作为参数（把JWT管理器绑定到 Flask 应用上）。
jwt = JWTManager(app)

# Fixed user lookup - handle string type user ID
# JWT = JSON Web Token 是一种“令牌（token）”格式，用来让前端和后端安全地证明“某个用户是谁”。
# JWT（JSON Web Token）本质上是一个由三部分组成的 JSON：
# HEADER.PAYLOAD.SIGNATURE
# 其中 payload（载荷） 是一组键值对。 下面的参数jwt_data就是payload.（jwt_data可以改名字，参数的位置才决定它的意义）
# sub 表示“用户身份（subject）”的固定字段（通常是 user_id）
@jwt.user_lookup_loader # 这是一个装饰器（decorator）, 告诉 Flask-JWT-Extended 框架 “当请求带有 JWT 时，如何根据 token 中的用户 ID 找回数据库里的用户对象”。
def user_lookup_callback(_jwt_header, jwt_data): # 为什么变量名前面有下划线 _ ? 这是 Python 的一种命名约定，意思是：“这个变量是存在的，但我们暂时不打算用它。” 其实等价于告诉别人：“框架会传给我两个参数，但我只关心第二个。”
    identity = jwt_data["sub"]  # This is a string
    return Guest.query.get(int(identity))  # Convert to integer for query
    # return DBTable对应的Class.query.get(int(identity))
# 这一段类似于样板代码 boilerplate


# Initialize database
def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # 当执行这行时，SQLAlchemy 会读取所有 db.Model 的类结构，
        # 在数据库中执行相应的 SQL 语句，例如：
        # CREATE TABLE guests (
        #     id INTEGER PRIMARY KEY,
        #     first_name VARCHAR(80), ......
        # );

        # sample rooms
        sample_rooms = [
            RoomType(
                name="Single Room",
                description="Comfortable single room with basic amenities",
                price_per_night=99.99,
                max_occupancy=1,
                amenities="Wi-Fi,TV,Air Conditioning"
            ),
            RoomType(
                name="Double Room",
                description="Spacious double room perfect for couples",
                price_per_night=149.99,
                max_occupancy=2,
                amenities="Wi-Fi,TV,Air Conditioning,Mini Bar"
            ),
            RoomType(
                name="Suite",
                description="Luxurious suite with separate living area",
                price_per_night=249.99,
                max_occupancy=4,
                amenities="Wi-Fi,TV,Air Conditioning,Mini Bar,Jacuzzi,Sea View"
            )
        ]

        # 插入sample数据
        db.session.add_all(sample_rooms)
        db.session.commit()

        print("✅ Database initialization completed")

init_database()


# Helper function: Get current user
def get_current_guest():
    user_id = get_jwt_identity()  # Now returns string
    return Guest.query.get(int(user_id))  # Convert to integer for query


# ========== Authentication Endpoints ==========
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()   # 从请求体中提取 JSON 数据。from flask import Flask, request, jsonify
        # 这里的 “请求体（body）” 就是前端（或 Postman）POST 请求里的 JSON 数据部分。

        required_fields = ['firstName', 'lastName', 'email', 'password'] # 这是一 个包含四个字符串元素的 Python list 列表。
        for field in required_fields:
            if field not in data or not data[field]: #如果某个字段缺失（not in data）或为空（not data[field]），就返回错误信息。
                return jsonify({'error': f'{field} is required'}), 400

        # .query.filter_by(email=...) 是查询语句，相当于 SQL：
        # SELECT * FROM guest WHERE email = 'xxx@example.com' LIMIT 1;
        if Guest.query.filter_by(email=data['email']).first(): # 在 Python 中：None 被视为 False; 任何对象（例如 <Guest 1>）都被视为 True
            return jsonify({'error': 'Email already registered'}), 400

        # 用传入的数据创建一个新的 Guest 实例
        guest = Guest(
            first_name=data['firstName'],
            last_name=data['lastName'],
            email=data['email']
        )
        guest.set_password(data['password'])

        db.session.add(guest) # 把对象加入“会话缓存（session）”，但还没写入数据库。
        db.session.commit() # 真正对数据库执行 SQL
        # INSERT INTO guests (first_name, last_name, email, password_hash)
        # VALUES ('John', 'Doe', 'john@example.com', 'pbkdf2:sha256:260000$...')

        # 这里返回的是一个 tuple（二元组），Flask 框架会自动把这个 tuple 转换成一个 HTTP Response 对象（真正发给客户端的）
        # Flask 会识别 (response, status_code) 格式，然后把它「封装」成真正的 HTTP 响应对象。
        return jsonify({
            'message': 'Registration successful',
            'guest': guest.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback() # 回滚事务，避免数据库半写入状态。
        return jsonify({'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400

        guest = Guest.query.filter_by(email=data['email']).first()

        if guest and guest.check_password(data['password']):
            # Convert user ID to string
            access_token = create_access_token(identity=str(guest.id))
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'guest': guest.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========== Room Related Endpoints ==========
@app.route('/api/rooms/available', methods=['GET'])
def get_available_rooms():
    try:
        check_in = request.args.get('checkInDate')
        check_out = request.args.get('checkOutDate')
        room_type = request.args.get('roomType')
        max_price = request.args.get('maxPrice')

        if not check_in or not check_out:
            return jsonify({'error': 'checkInDate and checkOutDate are required'}), 400

        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        if check_in_date >= check_out_date:
            return jsonify({'error': 'checkOutDate must be after checkInDate'}), 400

        if check_in_date < date.today():
            return jsonify({'error': 'checkInDate cannot be in the past'}), 400

        # Find booked rooms
        # from sqlalchemy import and_, or_, not_
        booked_rooms_subquery = db.session.query(Reservation.room_type_id).filter(
            and_(
                Reservation.status == 'Confirmed',
                Reservation.check_in_date < check_out_date,     # 你打算退房的时间 别人已经预定入住(根据reservation)
                Reservation.check_out_date > check_in_date      # 你打算入住的时间 别人还没退房(Reservation.check_out_date在你的check_in_date之后)
            )
        )

        # Find available rooms
        available_rooms_query = RoomType.query.filter(
            not_(RoomType.id.in_(booked_rooms_subquery))    # .in_() 是 SQLAlchemy 列对象（Column） 的方法，用来生成 SQL 的 IN 子句
        )

        if room_type:                                       # 如果用户输入了房型名称
            available_rooms_query = available_rooms_query.filter(
                RoomType.name.ilike(f'%{room_type}%')       # 用来执行 不区分大小写的模糊匹配，相当于 SQL 中的：WHERE name ILIKE '%room_type%'
            )

        if max_price:
            try:
                max_price_float = float(max_price)
                available_rooms_query = available_rooms_query.filter(
                    RoomType.price_per_night <= max_price_float
                )
            except ValueError:
                return jsonify({'error': 'maxPrice must be a valid number'}), 400

        available_rooms = available_rooms_query.all()

        return jsonify({
            'checkInDate': check_in,
            'checkOutDate': check_out,
            'availableRooms': [room.to_dict() for room in available_rooms]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rooms/<int:room_type_id>', methods=['GET'])
def get_room_details(room_type_id):
    try:
        room_type = RoomType.query.get_or_404(room_type_id)
        return jsonify(room_type.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========== Reservation Related Endpoints ==========
@app.route('/api/reservations', methods=['POST'])
@jwt_required()
def make_reservation():
    try:
        current_guest = get_current_guest()
        if not current_guest:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        print(f"📦 Received reservation request: {data}")  # Debug log

        required_fields = ['roomTypeId', 'checkInDate', 'checkOutDate', 'numberOfGuests']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        try:
            check_in_date = datetime.strptime(data['checkInDate'], '%Y-%m-%d').date()
            check_out_date = datetime.strptime(data['checkOutDate'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        if check_in_date >= check_out_date:
            return jsonify({'error': 'checkOutDate must be after checkInDate'}), 400

        if check_in_date < date.today():
            return jsonify({'error': 'checkInDate cannot be in the past'}), 400

        room_type = RoomType.query.get(data['roomTypeId'])
        if not room_type:
            return jsonify({'error': 'Room type not found'}), 404

        print(f"🔍 Checking room {room_type.name} availability from {check_in_date} to {check_out_date}")  # Debug log

        # Check if room is available
        existing_reservation = Reservation.query.filter(
            and_(
                Reservation.room_type_id == data['roomTypeId'],
                Reservation.status == 'Confirmed',
                Reservation.check_in_date < check_out_date,
                Reservation.check_out_date > check_in_date
            )
        ).first()

        if existing_reservation:
            print(f"❌ Room already booked: Reservation ID {existing_reservation.id}")  # Debug log
            return jsonify({'error': 'Room is not available for the selected dates'}), 400

        if data['numberOfGuests'] > room_type.max_occupancy:
            return jsonify({'error': f'This room can accommodate maximum {room_type.max_occupancy} guests'}), 400

        # Calculate total price
        nights = (check_out_date - check_in_date).days
        total_price = nights * room_type.price_per_night

        print(f"💰 Price calculation: {nights} nights × ${room_type.price_per_night} = ${total_price}")  # Debug log

        # Create reservation
        reservation = Reservation(
            guest_id=current_guest.id,
            room_type_id=data['roomTypeId'],
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=data['numberOfGuests'],
            total_price=total_price,
            status='Confirmed'
        )

        db.session.add(reservation)
        db.session.commit()

        print(f"✅ Reservation created successfully: Reservation ID {reservation.id}")  # Debug log

        return jsonify({
            'message': 'Reservation confirmed successfully',
            'reservation': reservation.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"💥 Reservation error: {str(e)}")  # Debug log
        return jsonify({'error': str(e)}), 500


@app.route('/api/my-bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    try:
        current_guest = get_current_guest()
        if not current_guest:
            return jsonify({'error': 'User not found'}), 404

        reservations = Reservation.query.filter_by(guest_id=current_guest.id).order_by(Reservation.created_at.desc()).all()

        return jsonify({
            'bookings': [reservation.to_dict() for reservation in reservations]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reservations/<int:reservation_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_reservation(reservation_id):
    try:
        current_guest = get_current_guest()
        if not current_guest:
            return jsonify({'error': 'User not found'}), 404

        reservation = Reservation.query.filter_by(
            id=reservation_id,
            guest_id=current_guest.id
        ).first_or_404()

        if reservation.check_in_date <= date.today():
            return jsonify({'error': 'Cannot cancel reservation on or after check-in date'}), 400

        reservation.status = 'Cancelled'
        db.session.commit()

        return jsonify({
            'message': 'Reservation cancelled successfully',
            'reservation': reservation.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Hotel Booking API is running'})


@app.route('/api/debug-simple-reservation', methods=['POST'])
def debug_simple_reservation():
    """Simplest reservation test, bypassing all validations"""
    try:
        # Manually create a reservation without checking any conditions
        reservation = Reservation(
            guest_id=1,  # Assume user ID is 1
            room_type_id=1,
            check_in_date=date(2026, 2, 1),
            check_out_date=date(2026, 2, 3),
            number_of_guests=1,
            total_price=199.98,
            status='Confirmed'
        )

        db.session.add(reservation)
        db.session.commit()

        return jsonify({
            'message': 'DEBUG: Simple reservation created successfully!',
            'reservation_id': reservation.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'DEBUG error: {str(e)}'}), 500


# Test endpoint
@app.route('/api/test-reservation', methods=['POST'])
@jwt_required()
def test_reservation():
    try:
        current_guest = get_current_guest()
        data = request.get_json()

        # Simplified: directly create reservation without availability check
        reservation = Reservation(
            guest_id=current_guest.id,
            room_type_id=1,  # Fixed room type
            check_in_date=date(2026, 2, 1),
            check_out_date=date(2026, 2, 3),
            number_of_guests=1,
            total_price=199.98,
            status='Confirmed'
        )

        db.session.add(reservation)
        db.session.commit()

        return jsonify({
            'message': 'Test reservation created successfully',
            'reservation': reservation.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Test failed: {str(e)}'}), 500


# Token debug endpoint
@app.route('/api/debug-token', methods=['GET'])
@jwt_required()
def debug_token():
    user_id = get_jwt_identity()
    current_guest = get_current_guest()
    return jsonify({
        "user_id": user_id,
        "user_id_type": type(user_id).__name__,
        "current_guest": current_guest.to_dict() if current_guest else None,
        "message": "Token debug info"
    })


if __name__ == '__main__':
    # print("🚀 Hotel Booking Platform API Service Starting...")
    # print("📝 Available Endpoints:")
    # print("   POST /api/register - User Registration")
    # print("   POST /api/login - User Login")
    # print("   GET  /api/rooms/available - Search Available Rooms")
    # print("   GET  /api/rooms/<id> - Room Details")
    # print("   POST /api/reservations - Create Reservation")
    # print("   GET  /api/my-bookings - My Bookings")
    # print("   POST /api/reservations/<id>/cancel - Cancel Reservation")
    # print("   GET  /api/debug-token - Debug Token")
    app.run(debug=True, host='0.0.0.0', port=5000)