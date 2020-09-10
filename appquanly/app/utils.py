from app import dao, app
from datetime import datetime
from flask import session
import csv
import os


def export_csv():
    hoso = dao.read_hoso()
    p = os.path.join(app.root_path, "data/hoso-%s.csv" % str(datetime.now()))
    with open(p, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "sdt",
                                               "diachi", "idquan", "ngaytiepnhan","email","tienno","loaidaily_id"])
        writer.writeheader()
        for hoso in hoso:
            writer.writerow(hoso)

    return p


def upload_avatar(file):
    path = "images/avatar/" + file.filename
    file.save(os.path.join(app.root_path, "static/", path))

    return path




