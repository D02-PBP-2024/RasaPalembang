from django.test import TestCase, Client
from restoran.models import Restoran
from authentication.models import User
from ulasan.models import Ulasan


class mainTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="UserDummy")
        self.restoran = Restoran.objects.create(
            nama="Restoran Dummy",
            user=self.user,
        )
        self.ulasan = Ulasan.objects.create(
            user=self.user,
            restoran=self.restoran,
            nilai=5,
        )

    def test_ulasan_url_is_exist(self):
        response = Client().get(f"/restoran/{self.restoran.id}/ulasan/")
        self.assertEqual(response.status_code, 200)

    def test_ulasan_object_is_exist(self):
        response = Client().get(f"/restoran/{self.restoran.id}/ulasan/")
        data = response.json()
        self.assertEqual(data[0]["id"], str(self.ulasan.id))
        self.assertEqual(data[0]["user"]["nama"], str(self.user.nama))
        self.assertEqual(data[0]["nilai"], self.ulasan.nilai)

    def test_tambah_ulasan_no_login(self):
        response = Client().get("/restoran/tambah/")
        self.assertEqual(response.status_code, 302)

    def test_edit_ulasan_no_login(self):
        response = Client().get(f"/restoran/{self.restoran.id}/ubah/")
        self.assertEqual(response.status_code, 302)

    def test_hapus_ulasan_no_login(self):
        response = Client().get(f"/restoran/{self.restoran.id}/hapus/")
        self.assertEqual(response.status_code, 302)
