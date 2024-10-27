from django.test import TestCase, Client
from minuman.models import Minuman
from restoran.models import Restoran
from authentication.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class mainTest(TestCase):
    def setUp(self):
        self.nama = "Minuman Dummy"
        self.restoran = Restoran.objects.create(
            nama="Restoran Dummy",
            user=User.objects.create_user(username="UserDummy")
        )

        image_data = b'1010'
        image_file = SimpleUploadedFile(
            name='dummy_image.jpg',
            content=image_data,
            content_type='image/jpeg'
        )

        self.minuman = Minuman.objects.create(
            nama=self.nama,
            harga=1000,
            deskripsi="",
            ukuran="BESAR",
            gambar=image_file,
            tingkat_kemanisan=0,
            restoran=self.restoran
        )
    def test_show_minuman_url_is_exist(self):
        response = Client().get("/minuman/")
        self.assertEqual(response.status_code, 200)

    def test_show_minuman_by_id_url_is_exist(self):
        response = Client().get(f"/minuman/{self.minuman.id}/")
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_page(self):
        response = Client().get("/minuman/nonfound/")
        self.assertEqual(response.status_code, 404)

    def test_create_minuman(self):
        self.assertEqual(self.minuman.nama, self.nama)

    def test_tambah_minuman_no_login(self):
        response = self.client.get("/minuman/tambah/")
        self.assertEqual(response.status_code, 302)

    def test_edit_minuman_no_login(self):
        response = self.client.get(f"/minuman/{self.minuman.id}/ubah/")
        self.assertEqual(response.status_code, 302)

    def test_hapus_minuman_no_login(self):
        response = self.client.get(f"/minuman/{self.minuman.id}/hapus/")
        self.assertEqual(response.status_code, 302)