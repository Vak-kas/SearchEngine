from django import forms

class SoloCollectorForm(forms.Form):
    url = forms.URLField(
        label='URL',
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter the URL'}),
        required=True
    )
