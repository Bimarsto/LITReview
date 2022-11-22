from django.shortcuts import render, redirect
from follows.models import UserFollows
from follows.forms import FollowForm
from authentication.models import User


def index(request):
    form = FollowForm()
    follows = UserFollows.objects.filter(user=request.user)
    followed_by = UserFollows.objects.filter(followed_user=request.user)
    message = ''
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            user_to_follow = form.cleaned_data['followed_user']
            if User.objects.filter(username=user_to_follow):
                user_to_follow = User.objects.get(username=user_to_follow)
                UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            else:
                message = "Nom d'utilisateur introuvable. Veuillez réessayer."
                return render(request,
                  'follows/index.html',
                  {'follows': follows,
                   'followed_by': followed_by,
                   'form': form,
                   'message' : message,
                   })
        return redirect('follows')
    return render(request,
                  'follows/index.html',
                  {'follows': follows,
                   'followed_by': followed_by,
                   'form': form,
                   'message' : message,
                   })


def unfollow(request, id_deleted):
    UserFollows.objects.get(user=request.user, id=id_deleted).delete()
    return redirect('follows')
