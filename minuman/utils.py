import re
from restoran.utils import restoran_data


# Method untuk mengembalikan data minuman
def minuman_data(minuman, message=None):
    data = {
        "pk": minuman.pk,
        "fields": {
            "nama": minuman.nama,
            "harga": minuman.harga,
            "deskripsi": minuman.deskripsi,
            "gambar": minuman.gambar.url if minuman.gambar else "",
            "ukuran": minuman.ukuran,
            "tingkat_kemanisan": minuman.tingkat_kemanisan,
            "restoran": restoran_data(minuman.restoran),
        }
    }

    if message is not None:
        data["message"] = message

    return data


# Method untuk validasi input harga, tingkat_kemanisan, dan ukuran
def validasi_input(harga, ukuran, tingkat_kemanisan):
    # Harga yang valid adalah 0 dan bilangan bulat positif
    harga_pattern = r"^[0-9]\d*$"
    # Tingkat kemanisan yang valid adalah bilangan bulat 0-100
    tingkat_kemanisan_pattern = r"^0*(?:[0-9][0-9]?|100)$"

    # Memastikan input harga dan tingkat_kemanisan dan ukuran valid
    message = ""
    if not re.match(harga_pattern, harga):
        message += "harga"

    if ukuran != "KECIL" and ukuran != "SEDANG" and ukuran != "BESAR":
        if message != "":
            message += " dan ukuran"
        else:
            message += "ukuran"

    if not re.match(tingkat_kemanisan_pattern, tingkat_kemanisan):
        if message != "":
            message += " dan tingkat_kemanisan"
        else:
            message += "tingkat_kemanisan"

    return message
