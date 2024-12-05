# Method untuk mengembalikan response dalam format yang sama
def format_response(success, message, data=None):
    response = {
        "success": success,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return response


# Method untuk mengembalikan data user yang diperlukan
def user_data(user):
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

    return data
