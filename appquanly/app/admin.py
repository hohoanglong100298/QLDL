from app import admin, db
from flask_admin.contrib.sqla import ModelView
from app.models import *



admin.add_view(ModelView(Loaidaily, db.session,name="Loại đại lý"))
admin.add_view(ModelView(Hoso, db.session,name="Hồ sơ"))
admin.add_view(ModelView(Phieuthutien, db.session,name="Phiếu thu"))
admin.add_view(ModelView(Doanhso, db.session,name="Doanh số"))
admin.add_view(ModelView(Congno, db.session,name="Công nợ"))
admin.add_view(ModelView(Phieuxuathang, db.session,name="Phiếu xuất"))
admin.add_view(ModelView(Mathang, db.session,name="Mặt hàng"))
admin.add_view(ModelView(Chitietxuathang, db.session,name="Chi tiết xuất hàng"))
admin.add_view(ModelView(Quydinhmathang, db.session,name="Quy định mặt hàng"))
admin.add_view(ModelView(Quychetochuc, db.session,name="Quy chế"))
admin.add_view(ModelView(Quydinhtienno, db.session,name="Quy định tiền nợ"))
admin.add_view(AboutUsView(name="Giới thiệu"))
