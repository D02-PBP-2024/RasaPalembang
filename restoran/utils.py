import re


# Method untuk mengembalikan data restoran
def restoran_data(restoran, message=None):
    """
    Mengembalikan representasi data restoran dalam format dictionary.
    """
    data = {
        "pk": restoran.pk,
        "fields": {
            "nama": restoran.nama,
            "alamat": restoran.alamat,
            "jam_buka": restoran.jam_buka.strftime('%H:%M'),
            "jam_tutup": restoran.jam_tutup.strftime('%H:%M'),
            "nomor_telepon": restoran.nomor_telepon if restoran.nomor_telepon else "",
            "gambar": restoran.gambar.url if restoran.gambar else "",
            "user": restoran.user.username,  # Username pemilik restoran
        }
    }

    if message is not None:
        data["message"] = message

    return data


def validasi_input(nama, alamat, jam_buka, jam_tutup):
    """
    Memvalidasi input data restoran, termasuk nama, alamat, jam buka, dan jam tutup.

    :param nama: Nama restoran
    :param alamat: Alamat restoran
    :param jam_buka: Jam buka restoran
    :param jam_tutup: Jam tutup restoran
    :return: Pesan kesalahan jika ada input yang tidak valid
    """
    message = ""

    # Validasi nama restoran
    if not nama or len(nama.strip()) == 0:
        message += "Nama restoran tidak boleh kosong. "
    
    # Validasi alamat restoran
    if not alamat or len(alamat.strip()) == 0:
        if message:
            message += "Alamat restoran tidak boleh kosong. "
        else:
            message += "Alamat restoran tidak boleh kosong."

    # Validasi jam buka dan jam tutup
    try:
        jam_buka = int(jam_buka.split(':')[0])
        jam_tutup = int(jam_tutup.split(':')[0])
        if jam_buka >= jam_tutup:
            if message:
                message += "Jam buka tidak boleh lebih besar atau sama dengan jam tutup. "
            else:
                message += "Jam buka tidak boleh lebih besar atau sama dengan jam tutup."
    except ValueError:
        if message:
            message += "Format waktu tidak valid. "
        else:
            message += "Format waktu tidak valid."

    return message
