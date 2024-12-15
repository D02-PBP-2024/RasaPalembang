# Method untuk mengembalikan data user yang diperlukan
def user_data(user, message=None):
    data = {
        "pk": user.pk,
        "username": user.username,
        "nama": user.nama,
        "deskripsi": user.deskripsi,
        "peran": user.peran,
        "foto": user.foto.url if user.foto else "",
        "poin": user.poin,
        "date_joined": user.date_joined,
    }
    if message is not None:
        data["message"] = message
    return data
