from app import app, db
from app.models import *
from functools import wraps
import json
import os
import hashlib


def read_hoso(keyword=None):
    q = Hoso.query

    if keyword:
        q = q.filter(Hoso.name.contains(keyword))
    return q.all()

def read_hoso_by_id(hoso_id):
    hoso = read_hoso()
    for p in hoso:
        if p["id"] == hoso_id:
            return p

    return None


def read_loaidaily():
    return Loaidaily.query.all()




def del_hoso(hoso_id):
    hoso = read_hoso()

    for idx, p in enumerate(hoso):
        if p["id"] == hoso_id:
            del hoso[idx]
            break

    return update_hoso_json(hoso)



def update_hoso(hoso_id, name, sdt, diachi, idquan, ngaytiepnhan,tienno,loaidaily):
    hoso = read_hoso()
    for idx, p in enumerate(hoso):
        if p["id"] == int(hoso_id):
            hoso[idx]["name"] = name
            hoso[idx]["sdt"] = sdt
            hoso[idx]["idquan"] = idquan
            hoso[idx]["ngaytiepnhan"] = datetime(ngaytiepnhan)
            hoso[idx]["tienno"] = float(tienno)
            hoso[idx]["loaidaily_id"] = int(loaidaily)

            break

    return update_hoso_json(hoso)



def delete_hoso(hoso_id):
    hoso = read_hoso()
    for idx, p in enumerate(hoso):
        if p["id"] == int(hoso_id):
            del hoso[idx]
            break

    return update_hoso(hoso)


def add_hoso(hoso_id, name, sdt, diachi, idquan, ngaytiepnhan,tienno,loaidaily):
    hoso = read_hoso()
    hoso.append({
        "id" : len(hoso) + 1,
        "name" : name,
        "sdt" : sdt,
        "idquan" : idquan,
        "ngaytiepnhan" : ngaytiepnhan,
        "tienno" : tienno,
        "loaidaily_id" : int(loaidaily)
    })

    return update_hoso_json(hoso)


def update_hoso_json(hoso):
    try:
        with open(os.path.join(app.root_path, "data/hoso.json"), "w", encoding="utf-8") as f:
            json.dump(hoso, f, ensure_ascii=False, indent=4)

        return True
    except Exception as ex:
        print(ex)
        return False


def read_loaidaily():
    return Loaidaily.query.all()


def read_hoso_by_cate_id(cate_id):
    return Loaidaily.query.get(cate_id).hoso


def load_users():
    with open(os.path.join(app.root_path, "data/users.json"), encoding="utf-8") as f:
        return json.load(f)


def add_user(name, username, password):
    user = User(name=name,
                username=username,
                password=str(hashlib.md5(password.strip().encode("utf-8")).hexdigest()))
    db.session.add(user)
    db.session.commit()

    return user

def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return User.query.filter(User.username == username,
                             User.password == password).first()




def get_user_by_id(user_id):
    return User.query.get(user_id)



if __name__ == "__main__":
    print(read_hoso())