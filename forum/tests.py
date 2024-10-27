from django.test import TestCase, Client
from authentication.models import User
from forum.models import Forum, Balasan
from restoran.models import Restoran


class mainTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="UserDummy")

        self.restoran = Restoran.objects.create(
            nama="Restoran Dummy",
            user=self.user,
        )

        self.forum = Forum.objects.create(
            topik="Topik Dummy",
            pesan="Pesan Dummy",
            restoran=self.restoran,
            user=self.user,
        )

        self.balasan = Balasan.objects.create(
            pesan="",
            forum=self.forum,
            user=self.user,
        )

    def test_show_forum_url_is_exist(self):
        response = Client().get(f"/restoran/{self.restoran.id}/forum/")
        self.assertEqual(response.status_code, 200)

    def test_show_forum_by_id_url_is_exist(self):
        response = Client().get(f"/restoran/{self.restoran.id}/forum/{self.forum.id}/")
        self.assertEqual(response.status_code, 200)

    def test_tambah_forum_no_login(self):
        response = Client().get(f"/restoran/{self.restoran.id}/forum/tambah/")
        self.assertEqual(response.status_code, 302)

    def test_balasan_forum_no_login(self):
        response = Client().get(f"/restoran/{self.restoran.id}/forum/{self.forum.id}/balas")
        self.assertEqual(response.status_code, 302)

    def test_delete_forum_no_login(self):
        response = Client().get(f"/restoran/{self.restoran.id}/forum/{self.forum.id}/delete_forum")
        self.assertEqual(response.status_code, 302)

    def test_delete_balasan_forum_no_login(self):
        response = Client().get(f"/restoran/{self.restoran.id}/forum/{self.forum.id}/delete_balasan/{self.balasan.id}")
        self.assertEqual(response.status_code, 302)