from django.forms import ModelForm, RadioSelect, Select, forms
from contributions.models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre',
                  }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre',
                  'rating': 'Note',
                  'body': 'Commentaire',
                  }
