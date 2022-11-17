from django.shortcuts import render, redirect
from follows.models import UserFollows
from authentication.models import User


def index(request):
    follows = UserFollows.objects.filter(user=request.user)
    followed_by = UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'follows/index.html', context={'follows': follows, 'followed_by': followed_by})


def delete(request, id_deleted):
    UserFollows.objects.get(user=request.user, id=id_deleted).delete()
    return redirect('follows')
