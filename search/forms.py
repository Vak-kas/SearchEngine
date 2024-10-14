from django import forms

class SearchForm(forms.Form):
    search_term = forms.CharField(label='검색어', max_length=100)
