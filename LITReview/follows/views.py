from django.shortcuts import render
from follows.models import UserFollows


def index(request):
    follows = UserFollows.objects.filter(user=request.user)
    followed_by = UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'follows/index.html', context={'follows': follows, 'followed_by': followed_by})
