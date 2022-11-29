"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from LITReview import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from authentication.views import signup, login_page, logout_page
from follows.views import index, unfollow
from contributions.views import flux, posts, \
    add_ticket, edit_ticket, delete_ticket,\
    add_review_without_ticket, add_review_from_ticket, edit_review, delete_review

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', flux, name='index'),
    path('posts/', posts, name='posts'),
    path('login/', login_page, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_page, name='logout'),
    path('follows/', index, name='follows'),
    path('unfollows/<int:id_deleted>/', unfollow, name='unfollow'),
    path('tickets/add/', add_ticket, name='add_ticket'),
    path('tickets/edit/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('tickets/delete/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('reviews/add/', add_review_without_ticket, name='add_review_without_ticket'),
    path('reviews/<int:ticket_id>/add/', add_review_from_ticket, name='add_review_from_ticket'),
    path('reviews/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', delete_review, name='delete_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
