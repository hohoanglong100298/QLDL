from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from app import db
from flask_admin import BaseView, expose
from datetime import datetime
from flask_login import UserMixin
import enum





class Loaidaily(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False)
    hoso = relationship('Hoso', backref="loaidaily", lazy=True)


    def __str__(self):
        return self.name

class Hoso(db.Model):

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    sdt = Column(String(255), nullable=True)
    diachi = Column(String(255), nullable=True)
    idquan = Column(String(255), nullable=True)
    ngaytiepnhan = Column(DateTime, default=datetime.now())
    email = Column(String(255), nullable=True)
    tienno = Column(Float, default=0)
    loaidaily_id = Column(Integer, ForeignKey(Loaidaily.id), nullable=False)

    phieuthutien = relationship('Phieuthutien', backref = "hoso", lazy = True)
    doanhso = relationship('Doanhso', backref="hoso", lazy=True)
    congno = relationship('Congno', backref="hoso", lazy=True)
    phieuxuathang = relationship('Phieuxuathang', backref="hoso", lazy=True)



class Phieuthutien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaythutien = Column(DateTime, default=datetime.now())
    sotienthu = Column(Float, default=0)
    hoso_id = Column(Integer, ForeignKey(Hoso.id), nullable=False)



class Doanhso(db.Model):

    thang = Column(Integer, primary_key=True, autoincrement=True)
    sophieuxuat = Column(String(255),nullable=False)
    tonggiatri = Column(Float, default=8)
    hoso_id = Column(Integer, ForeignKey(Hoso.id), nullable=False)


class Congno(db.Model):

    thang = Column(Integer, primary_key=True, autoincrement=True)
    nodau = Column(Float, default=0)
    phatsinh = Column(Float, default=0)
    nocuoi = Column(Float, default=0)
    hoso_id = Column(Integer, ForeignKey(Hoso.id), nullable=False)



class Phieuxuathang(db.Model):

    id = Column(Integer, primary_key=True, autoincrement=True)
    ngaylapphieuxuat = Column(DateTime, default=datetime.now())
    hoso_id = Column(Integer, ForeignKey(Hoso.id), nullable=False)
    chitietxuathang = relationship('Chitietxuathang', backref="phieuxuathang", lazy=True)





class Mathang(db.Model):

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255),nullable=False)
    chitietxuathang = relationship('Chitietxuathang', backref="mathang", lazy=True)


class Chitietxuathang(db.Model):

    phieuxuathang_id = Column(Integer, ForeignKey(Phieuxuathang.id), primary_key=True)
    mathang_id = Column(Integer, ForeignKey(Mathang.id), primary_key=True)

    soluong = Column(Integer, nullable=False)
    dongia = Column(Float, default=8)
    donvitinh = Column(String(255), nullable=False)
    thanhtien = Column(Float, default=8)


class Quydinhmathang(db.Model):
    __tablename__ = "quydinhmathang"
    id = Column(Integer, primary_key=True, autoincrement=True)
    donvitinh = Column(String(255), nullable=False)
    dongia = Column(Float, default=0)

class Quychetochuc(db.Model):
    __tablename__ = "quychetochuc"
    id = Column(Integer, primary_key=True, autoincrement=True)
    soloaidaily = Column(String(255), nullable=False)
    sodailytoida = Column(String(255), nullable=False)
    somathang = Column(String(255), nullable=False)
    soquan = Column(String(255), nullable=False)

class Quydinhtienno(db.Model):
    __tablename__ = "quydinhtienno"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tiennotoida = Column(Float, default=0)


class AboutUsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/about-us.html')

class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    use_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name



if __name__== "__main__":
    db.create_all()
