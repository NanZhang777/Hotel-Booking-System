# 从 Flask-SQLAlchemy 模块中导入一个类 —— SQLAlchemy。
# SQLAlchemy 是一个“ORM 框架（对象关系映射工具）”，
# 它可以让你 不用写 SQL 语句，而是用 Python 类、对象来操作数据库。
from flask_sqlalchemy import SQLAlchemy

# 创建一个名为 db 的 SQLAlchemy 实例对象。
# 所有的数据库操作（定义表、增删改查）都要通过这个 db 来进行。
# 它是 Flask-SQLAlchemy 框架提供的一个“数据库接口”。
db = SQLAlchemy()