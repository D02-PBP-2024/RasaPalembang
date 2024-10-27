from django.test import TestCase, Client
from restoran.models import Restoran
from authentication.models import User


class mainTest(TestCase):
    def setUp(self):
        self.nama = "Restoran Dummy"
        self.restoran = Restoran.objects.create(
            nama=self.nama,
            user=User.objects.create_user(username="UserDummy")
        )

    def test_restoran_url_is_exist(self):
        response = Client().get("/restoran/")
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_page(self):
        response = Client().get("/restoran/nonfound/")
        self.assertEqual(response.status_code, 404)

    def test_create_restoran(self):
        self.assertEqual(self.restoran.nama, self.nama)

    def test_restoran_by_id_url_is_exist(self):
        response = Client().get(f"/restoran/{self.restoran.id}/")
        self.assertEqual(response.status_code, 200)

    def test_tambah_restoran_no_login(self):
        response = Client().get("/restoran/tambah/")
        self.assertEqual(response.status_code, 302)

    def test_edit_restoran_no_login(self):
        response = Client().get(f"/restoran/{self.restoran.id}/ubah/")
        self.assertEqual(response.status_code, 302)

    def test_delete_restoran_no_login(self):
        response = Client().get(f"/restoran/{self.restoran.id}/hapus/")
        self.assertEqual(response.status_code, 302)
