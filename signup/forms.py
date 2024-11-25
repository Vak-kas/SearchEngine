from django import forms
from .models import User, Category

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'interests']
        widgets = {
            'password': forms.PasswordInput(),
        }

    interests = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # 선택이 필수가 아닌 경우
    )
