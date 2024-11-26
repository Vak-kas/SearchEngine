from django.shortcuts import render, redirect
from .forms import UserSignupForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password


#회원 가입 기능
def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # 해싱과정
            user.save()
            form.save_m2m()  # 다대다 관계 저장
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('login')  # 로그인 페이지로 리디렉션
        else:
            messages.error(request, '회원가입에 실패했습니다. 다시 시도해주세요.')
    else:
        form = UserSignupForm()

    return render(request, 'signup/signup.html', {'form': form})
