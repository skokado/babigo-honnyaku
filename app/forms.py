from django import forms


class InputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
