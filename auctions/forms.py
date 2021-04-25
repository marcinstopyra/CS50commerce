from django import forms
from .models import Categories

class create_listing_form(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=1000, widget=forms.Textarea)
    start_bid = forms.FloatField()
    photo = forms.URLField(required=False)
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), widget=forms.Select)

    title.widget.attrs.update({'placeholder':'Title'})
    description.widget.attrs.update({'placeholder':'product description', 'rows': 10, 'cols':100})
    start_bid.widget.attrs.update({'placeholder':'start bid', 'min': 0})
    photo.widget.attrs.update({'placeholder':'product photo url (optional)'})