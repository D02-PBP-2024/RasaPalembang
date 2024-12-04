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
            "restoran": makanan.restoran.pk,
            "kategori": [kategori.pk for kategori in makanan.kategori.all()],
        }
    }

    if message is not None:
        data["message"] = message

    return data

def validasi_input(harga, kalori):
    # Harga yang valid adalah 0 dan bilangan bulat positif
    harga_pattern = r"^[0-9]\d*$"
    # Kalori yang valid adalah bilangan bulat positif
    kalori_pattern = r"^[0-9]\d*$"

    # Memastikan input harga dan kalori valid
    message = ""
    if not re.match(harga_pattern, harga):
        message += "harga"
    
    if not re.match(kalori_pattern, kalori):
        if message != "":
            message += " dan kalori"
        else:
            message += "kalori"
    
    return message