from django import forms
from contributions.models import Ticket, Review


class TicketForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre',
                  }


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.RadioSelect(choices=(
        (0, "- 0"),
        (1, "- 1"),
        (2, "- 2"),
        (3, "- 3"),
        (4, "- 4"),
        (5, "- 5"))))

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
