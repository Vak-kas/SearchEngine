from django import forms

class CollectorForm(forms.Form):
    url = forms.URLField(label='URL', required=True, widget=forms.TextInput(attrs={'placeholder': 'URL 입력'}))
    collector_type = forms.ChoiceField(
        label='수집기 유형',
        choices=[
            ('scrapy', 'A (Scrapy)'),
            ('selenium', 'B (Selenium)'),
            ('solo', 'C (Solo)')
        ],
        widget=forms.RadioSelect
    )
