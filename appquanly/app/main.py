from flask import render_template, request, redirect, url_for, jsonify, send_file, session
from app import app, dao, utils, login_manager
from app.decorator import login_required
from flask_login import login_user
from app.models import *
from app.admin import *
import json
import hashlib


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hoso")
def hoso():
    return render_template("hoso.html")


@app.route("/api/hoso", methods=["get", "post"])
def api_hoso_list():
    if request.method == "POST":
        err = ""
        hoso_id = request.args.get("hoso_id")
        hoso = None
        if hoso_id:
            hoso = dao.read_hoso_by_id(hoso_id=int(hoso_id))

        if request.method.lower() == "post":
            if hoso_id:  # Cap nhat
                data = dict(request.form.copy())
                data["hoso_id"] = hoso_id
                if dao.update_hoso(**data):
                    return redirect(url_for("hoso_list"))
            else:  # Them

                import json
                hoso = dao.add_hoso(**dict(json.loads(request.data)))
                if hoso:
                    return jsonify(hoso)

            err = "Something wrong!!! Please back later!"

        return jsonify({"error_message": err})

    kw = request.args.get("keyword")

    return jsonify(dao.read_hoso(keyword=kw))


@app.route("/hoso/<int:loaidaily_id>")
def hoso_by_cate_id(loaidaily_id):
    return render_template("hoso.html",
                           hoso=dao.read_hoso(loaidaily_id=loaidaily_id))


@app.route("/hoso/add", methods=["get", "post"])
@login_required
def add_or_update_hoso():
    err = ""
    hoso_id = request.args.get("hoso_id")
    hoso = None
    if hoso_id:
        hoso = dao.read_hoso_by_id(hoso_id=int(hoso_id))

    if request.method.lower() == "post":
        # name = request.form.get("name")
        # price = request.form.get("price", 0)
        # images = request.form.get("images")
        # description = request.form.get("description")
        # category_id = request.form.get("category_id", 0)
        # import pdb
        # pdb.set_trace()
        if hoso_id:  # Cap nhat
            data = dict(request.form.copy())
            data["hoso_id"] = hoso_id
            if dao.update_hoso(**data):
                return redirect(url_for("hoso_list"))
        else:  # Them
            if dao.add_hoso(**dict(request.form)):
                return redirect(url_for("hoso_list"))

        err = "Something wrong!!! Please back later!"

    return render_template("product-add.html",
                           loaidaily=dao.read_loaidaily(),
                           hoso=hoso,
                           err=err)


@app.route("/api/hoso/<int:hoso_id>", methods=["delete"])
def delete_hoso(hoso_id):
    if dao.delete_hoso(hoso_id=hoso_id):
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": {"hoso_id": hoso_id}
        })

    return jsonify({
        "status": 500,
        "message": "Failed"
    })


@app.route("/hoso/export")
@login_required
def export_hoso():
    return send_file(utils.export_csv())


@app.route("/login", methods=["get", "post"])
def login():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.validate_user(username=username, password=password)
        if user:
            session["user"] = user

            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for("index"))
        else:
            err_msg = "DANG NHAP KHONG THANH CONG"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    session["user"] = None
    return redirect(url_for("index"))


@app.route("/register", methods=["get", "post"])
def register():
    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "The password does not match!"
        else:
            path = utils.upload_avatar(file=request.files["avatar"])
            if dao.add_user(name=name, username=username,
                            password=password, avatar=path):
                return redirect(url_for('login'))
            else:
                err_msg = "Something wrong!!!"

    return render_template("register.html", err_msg=err_msg)


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()

        if user:
            login_user(user=user)
    return redirect("/admin")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    app.run(debug=False, port=5050)
