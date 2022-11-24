from itertools import chain
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import CharField, Value
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review

RATING = [0, 1, 2, 3, 4, 5]

def add_ticket(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return HttpResponse('<h2>Ticket créer!</h2>')
    return render(request,
                  'contributions/ticket.html',
                  {'form': form,
                   'page_title': 'Créer un ticket',
                   })


def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,
                  'contributions/ticket.html',
                  {'form': form,
                   'page_title': 'Modifier votre ticket',
                   })


def add_review_without_ticket(request):
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
                  'contributions/add_review_without_ticket.html',
                  {'ticket_form': ticket_form,
                   'review_form': review_form,
                   })


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
                  'contributions/add_review_from_ticket.html',
                  {'ticket': ticket,
                   'review_form': review_form,
                   'page_title': 'Créer une critique'
                   })


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
                  'contributions/add_review_from_ticket.html',
                  {'review_form': form,
                   'ticket': ticket,
                   'page_title': 'Modifier votre critique',
                   })


def get_users_reviews(user):
    user_reviews = Review.objects.filter(user=user)
    return user_reviews


def get_all_reviews():
    all_reviews = Review.objects.all()
    return all_reviews


def get_users_tickets(user):
    user_tickets = Ticket.objects.filter(user=user)
    return user_tickets


def get_all_tickets():
    all_tickets = Ticket.objects.all()
    return all_tickets


def flux(request):
    reviews = get_all_reviews()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_all_tickets()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    all_posts = sorted(chain(tickets, reviews),
                   key=lambda post: post.time_created,
                   reverse=True)
    return render(request, 'contributions/index.html', {'posts': all_posts,
                                                        'rating': RATING})


def posts(request):
    reviews = get_users_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    user_posts = sorted(chain(tickets, reviews),
                   key=lambda post: post.time_created,
                   reverse=True)
    return render(request, 'contributions/posts.html', {'posts': user_posts,
                                                        'rating': RATING})
