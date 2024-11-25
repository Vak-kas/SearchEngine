from django import forms
from .models import User, Interest

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'interests']
        widgets = {
            'password': forms.PasswordInput(),
            'interests': forms.CheckboxSelectMultiple(),
        }

    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # 선택이 필수가 아닌 경우
    )

    
