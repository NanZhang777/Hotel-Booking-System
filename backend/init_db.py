# import os
# from app import app, db
# from models import Guest, RoomType
#
#
# def init_database():
#     # Delete existing database
#     if os.path.exists('hotel.db'):
#         os.remove('hotel.db')
#         print("🗑️  Old database deleted")
#
#     # Create new database
#     with app.app_context():
#         db.create_all()
#         print("✅ Database tables created successfully")
#
#         # Add sample room data
#         sample_rooms = [
#             RoomType(
#                 name="Single Room",
#                 description="Comfortable single room with basic amenities",
#                 price_per_night=99.99,
#                 max_occupancy=1,
#                 amenities="Wi-Fi,TV,Air Conditioning"
#             ),
#             RoomType(
#                 name="Double Room",
#                 description="Spacious double room perfect for couples",
#                 price_per_night=149.99,
#                 max_occupancy=2,
#                 amenities="Wi-Fi,TV,Air Conditioning,Mini Bar"
#             ),
#             RoomType(
#                 name="Suite",
#                 description="Luxurious suite with separate living area",
#                 price_per_night=249.99,
#                 max_occupancy=4,
#                 amenities="Wi-Fi,TV,Air Conditioning,Mini Bar,Jacuzzi,Sea View"
#             )
#         ]
#         db.session.add_all(sample_rooms)
#         db.session.commit()
#         print("✅ Sample room data added successfully")
#
#         print("🎉 Database initialization completed!")
#
#
# if __name__ == '__main__':
#     init_database()