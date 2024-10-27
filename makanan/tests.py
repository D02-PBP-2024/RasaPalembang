from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

import makanan
from makanan.models import Makanan
from restoran.models import Restoran
from authentication.models import User


class mainTest(TestCase):
    def setUp(self):
        self.nama = "Makanan Dummy"
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

        self.makanan = Makanan.objects.create(
            nama=self.nama,
            harga=1000,
            deskripsi="",
            gambar=image_file,
            kalori=0,
            restoran=self.restoran,
        )
    def test_makanan_url_is_exist(self):
        response = Client().get("/makanan/")
        self.assertEqual(response.status_code, 200)

    def test_create_makanan(self):
        self.assertEqual(self.makanan.nama, self.nama)

    def test_makanan_by_id_url_is_exist(self):
        response = Client().get(f"/makanan/{self.makanan.id}")
        self.assertEqual(response.status_code, 200)

    def test_tambah_makanan_no_login(self):
        response = self.client.get("/makanan/tambah/")
        self.assertEqual(response.status_code, 302)

    def test_edit_makanan_no_login(self):
        response = self.client.get(f"/makanan/{self.makanan.id}/edit")
        self.assertEqual(response.status_code, 302)
