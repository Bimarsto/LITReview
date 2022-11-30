from django import forms


class FollowForm(forms.Form):
    followed_user = forms.CharField(label='')
