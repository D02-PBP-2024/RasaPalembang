# Method untuk mengembalikan data favorit
def favorit_data(favorit, message=None):
    data = {
        "pk": favorit.id,
        "fields": {
            "catatan": favorit.catatan,
            "user": favorit.user.id,
            "makanan": favorit.makanan.id if favorit.makanan else None,
            "minuman": favorit.minuman.id if favorit.minuman else None,
            "restoran": favorit.restoran.id if favorit.restoran else None,
        }
    }

    if message is not None:
        data["message"] = message

    return data
