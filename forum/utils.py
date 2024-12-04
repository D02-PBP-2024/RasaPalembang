# Method untuk mengembalikan data forum
def forum_data(forum, message=None):
    data = {
        "pk": forum.pk,
        "fields": {
            "topik": forum.topik,
            "pesan": forum.pesan,
            "tanggal_posting": forum.tanggal_posting,
            "user": forum.user.pk,
            "restoran": forum.restoran.pk
        }
    }

    if message is not None:
        data["message"] = message

    return data

# Method untuk mengembalikan data balasan
def balasan_data(balasan, message=None):
    data = {
        "pk": balasan.pk,
        "fields": {
            "pesan": balasan.pesan,
            "tanggal_posting": balasan.tanggal_posting,
            "user": balasan.user.pk,
            "forum": balasan.forum.pk
        }
    }

    if message is not None:
        data["message"] = message

    return data
