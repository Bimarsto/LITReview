from django import forms
from django.forms import CharField
from follows.models import UserFollows


class FollowForm(forms.ModelForm):
    # followed_user = CharField(label='')
    class Meta:
        model = UserFollows
        fields = ['followed_user']

    # username = forms.CharField(label="")
