from django.shortcuts import render, redirect
from follows.models import UserFollows
from authentication.models import User
from follows.forms import FollowForm


def index(request):
    form = FollowForm()
    follows = UserFollows.objects.filter(user=request.user)
    followed_by = UserFollows.objects.filter(followed_user=request.user)
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            new_follow = form.save(commit=False)
            new_follow.user = request.user
            new_follow.save()
        return redirect('follows')
    return render(request,
                  'follows/index.html',
                  {'follows': follows,
                   'followed_by': followed_by,
                   'form': form})


def unfollow(request, id_deleted):
    UserFollows.objects.get(user=request.user, id=id_deleted).delete()
    return redirect('follows')
