function add_to_hoso(id, name, sdt, idquan,diachi, ngaytiepnhan, email, tienno, loaidaily_id) {
            fetch("/api/hoso", {
                method: "post",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: id,
                    name: name,
                    sdt: sdt,
                    idquan: idquan,
                    diachi: diachi,
                    ngaytiepnhan: ngaytiepnhan,
                    email: email,
                    tienno: tienno,
                    loaidaily_id: loaidaily_id

                })
            }).then(res => res.json()).then(data => {
                var hoso = document.getElementById("hosoId")
                hoso.innerText = data.quantity
            })
        }

        function delete_hoso(hosoId) {
            var c = confirm("Ban chac chan xoa khong?");
            if (c == true) {
                fetch("/api/hoso/" + hosoId, {
                    method: "delete"
                }).then(function(res) {
                    return res.json();
                }).then(function(data) {
                    console.info(data);
                    var hsId = data.data.hoso_id;
                    var p = document.getElementById("hoso" + hsId);
                    p.style.display = "none";
                }).catch(function(err) {
                    console.error(err);
                });
            }
        }