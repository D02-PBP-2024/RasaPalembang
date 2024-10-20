from django.forms import ModelForm
from forum.models import Forum, Balasan


class ForumForm(ModelForm):
    class Meta:
        model = Forum
        fields = ["topik", "pesan", "user", "restoran"]


class BalasanForm(ModelForm):
    class Meta:
        model = Balasan
        fields = ["pesan", "vote", "user", "forum"]
