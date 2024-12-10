import re


# Method untuk mengembalikan data ulasan
def ulasan_data(ulasan, message=None):
    data = {
        "pk": ulasan.pk,
        "fields": {
            "nilai": ulasan.nilai,
            "deskripsi": ulasan.deskripsi,
            "user": ulasan.user.username,
        }
    }

    if message is not None:
        data["message"] = message

    return data


# Method untuk validasi input nilai
def validasi_input(nilai):
    # Memastikan nilai adalah integer
    nilai = int(nilai)

    # Nilai yang valid adalah 0 sampai 5
    if nilai < 0 or nilai > 5:
        return "nilai"
    return ""
