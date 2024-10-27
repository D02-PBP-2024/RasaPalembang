from django.test import TestCase, Client

import favorit
from authentication.models import User
from favorit.models import Favorit
from restoran.models import Restoran


class mainTest(TestCase):
    def setUp(self):
        self.username = "UserDummy"
        self.password = "tes12345678"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in)

        self.favorit = Favorit.objects.create(
            user=self.user
        )

        self.restoran = Restoran.objects.create(
            nama="Restoran Dummy",
            user=User.objects.create_user(username="OwnerDummy")
        )

    def test_favorit_url_is_exist(self):
        response = self.client.get("/favorit/")
        self.assertEqual(response.status_code, 200)

    def test_tambah_favorit_no_login(self):
        response = Client().get(f"/favorit/tambah/makanan/{self.restoran.id}/")
        self.assertEqual(response.status_code, 302)

    def test_edit_favorit_no_login(self):
        response = Client().get(f"/favorit/ubah/{self.favorit.id}/")
        self.assertEqual(response.status_code, 302)

    def test_delete_favorit_no_login(self):
        response = Client().get(f"/favorit/hapus/{self.favorit.id}/")
        self.assertEqual(response.status_code, 302)