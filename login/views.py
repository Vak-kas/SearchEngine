from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '로그인에 성공했습니다.')
            return redirect('main')  # 로그인 후 리디렉션할 페이지 이름으로 변경 필요
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    return render(request, 'login/login.html')
