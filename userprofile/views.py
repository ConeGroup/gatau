from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from home.forms import RegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from userprofile.forms import EditProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.




@login_required
def show_userprofile(request):
    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A'
    }

    return render(request, "userprofile.html", context)


@login_required
@csrf_exempt
def edit_profile_ajax(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            response_data = {'message': 'Profil kamu berhasil diubah!'}
        else:
            response_data = {'message': 'Gagal mengubah profil. Cek isian form kamu.'}

        #return HttpResponse(response_data)

        return JsonResponse(response_data)
    else:
        user_form = EditProfileForm(instance=request.user)

    return render(request, 'userprofile.html', {'user_form': user_form})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            return redirect(to='userprofile.html')
    else:
        user_form = EditProfileForm(instance=request.user)

    return render(request, 'userprofile.html', {'user_form': user_form})








@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Ini biar session masih tetap aktif
            return redirect('userprofile.html')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



@login_required
def change_password_ajax(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Ini biar session masih tetap aktif
            print("oeyy")
            return JsonResponse({'message': 'Password kamu berhasil diubah!'})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})    