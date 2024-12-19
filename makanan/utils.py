from restoran.utils import restoran_data
import re


# Method untuk mengembalikan data makanan
def makanan_data(makanan, message=None):
    data = {
        "pk": makanan.pk,
        "fields": {
            "nama": makanan.nama,
            "harga": makanan.harga,
            "deskripsi": makanan.deskripsi,
            "gambar": makanan.gambar.url if makanan.gambar else "",
            "kalori": makanan.kalori,
            "restoran": restoran_data(makanan.restoran),
            "kategori": [kategori.pk for kategori in makanan.kategori.all()],
        },
    }

    if message is not None:
        data["message"] = message

    return data


def validasi_input(harga, kalori):
    # Harga dan kalori yang valid adalah 0 dan bilangan bulat positif
    harga_dan_kalori_pattern = r"^[0-9]\d*$"

    # Memastikan input harga dan kalori valid
    message = ""
    if not re.match(harga_dan_kalori_pattern, harga):
        message += "harga"

    if not re.match(harga_dan_kalori_pattern, kalori):
        if message != "":
            message += " dan kalori"
        else:
            message += "kalori"

    return message
