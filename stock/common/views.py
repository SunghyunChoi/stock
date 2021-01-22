from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # 이름 가져오기
            raw_password = form.cleaned_data.get('password1') # 비밀번호 가져오기
            user = authenticate(username=username, password=raw_password) # 회원가입 후 자동 로그인 : authenticate
            login(request, user)
            return redirect('mainboard:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})