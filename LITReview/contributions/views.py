from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import CharField, Value
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review
from follows.models import UserFollows

RATING = [0, 1, 2, 3, 4, 5]


@login_required
def add_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('index')
    return render(request,
                  'contributions/ticket.html',
                  {'form': form,
                   'page_title': 'Créer un ticket',
                   })


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,
                  'contributions/ticket.html',
                  {'form': form,
                   'ticket': ticket,
                   'page_title': 'Modifier votre ticket',
                   })


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user == request.user:
        if request.method == 'POST':
            ticket.delete()
            return redirect('posts')
    else:
        return render(request,
                      'contributions/delete_error.html',
                      {'type_item': "ticket"})
    return render(request,
                  'contributions/delete_item.html',
                  {'ticket': ticket,
                   'type_item': "ticket"})


@login_required
def add_review_not_from_ticket(request):
    user = request.user
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = user
            review.ticket = get_object_or_404(Ticket, id=ticket.id)
            review.save()
        else:
            return redirect('add_review_without_ticket')
        return redirect('index')
    return render(request,
                  'contributions/review_not_from_ticket.html',
                  {'ticket_form': ticket_form,
                   'review_form': review_form,
                   })


@login_required
def add_review_from_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = request.user
            form.save()
        return redirect('index')
    return render(request,
                  'contributions/review_from_ticket.html',
                  {'ticket': ticket,
                   'review_form': review_form,
                   'page_title': 'Créer une critique'
                   })


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    form = ReviewForm(instance=review)
    ticket = get_object_or_404(Ticket, id=review.ticket.id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,
                  'contributions/review_from_ticket.html',
                  {'review_form': form,
                   'ticket': ticket,
                   'page_title': 'Modifier votre critique',
                   })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        if request.method == 'POST':
            review.delete()
            return redirect('posts')
    else:
        return render(request,
                      'contributions/delete_error.html',
                      {'type_item': "review"})
    return render(request,
                  'contributions/delete_item.html',
                  {'review': review,
                   'type_item': "review"})


@login_required
def get_users_reviews(request, user):
    user_reviews = Review.objects.filter(user=user)
    return user_reviews


@login_required
def get_followed_user_reviews(request, users_followed):
    users_list = users_followed.values_list('followed_user_id')
    user_followed_reviews = Review.objects.filter(user__id__in=users_list)
    return user_followed_reviews


@login_required
def get_users_tickets(request, user):
    user_tickets = Ticket.objects.filter(user=user)
    return user_tickets


@login_required
def get_followed_user_tickets(request, users_followed):
    users_list = users_followed.values_list('followed_user_id')
    user_followed_tickets = Ticket.objects.filter(user__id__in=users_list)
    return user_followed_tickets


@login_required
def flux(request):
    users_followed = UserFollows.objects.filter(user=request.user)
    user_reviews = get_users_reviews(request, request.user)
    followed_user_reviews = get_followed_user_reviews(request, users_followed)
    reviews = user_reviews | followed_user_reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    user_tickets = get_users_tickets(request, request.user)
    followed_user_tickets = get_followed_user_tickets(request, users_followed)
    tickets = user_tickets | followed_user_tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    all_posts = sorted(chain(tickets, reviews),
                       key=lambda post: post.time_created,
                       reverse=True)
    return render(request, 'contributions/index.html', {'posts': all_posts,
                                                        'rating': RATING})


@login_required
def posts(request):
    reviews = get_users_reviews(request, request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_tickets(request, request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    user_posts = sorted(chain(tickets, reviews),
                        key=lambda post: post.time_created,
                        reverse=True)
    return render(request, 'contributions/posts.html', {'posts': user_posts,
                                                        'rating': RATING})
