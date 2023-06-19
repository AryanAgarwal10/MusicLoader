from django import forms
from musicals.models import Music


class MusicForm(forms.Form):
    music=forms.FileField()
    type=forms.ChoiceField(choices=[('private','Private'),
    ('public','Public'),
    ('protected','Protected')])
    title=forms.CharField(max_length=500, widget= forms.TextInput
                           (attrs={'placeholder':'Title'}))
    emails=forms.CharField(max_length=500, required=False, widget= forms.Textarea
                           (attrs={'rows':'7','placeholder':'Enter emails for protected access separated by new line'}))

