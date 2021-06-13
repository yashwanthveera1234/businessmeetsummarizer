from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, MailReceiverModelForm

from .models import MailReceiverModel

from django.contrib.auth.models import User




def registerView(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('Users:loginView')
    else:
        form=UserRegisterForm()
    return render(request, 'register.html', {'form':form})




def homeView(request):
    return render(request, 'home.html')




def profileView(request):
    user = User.objects.get(pk = request.user.id)
    mailReceiverObj = MailReceiverModel.objects.filter(user = user)

    if len(mailReceiverObj) == 0:
        m = MailReceiverModel(name = user.username, email = user.email, user = user)
        m.save()
    
    if request.method == 'POST':
        form = MailReceiverModelForm(request.POST)
        if form.is_valid():
            try:
                mr = MailReceiverModel(name = form.cleaned_data.get('name'), email = form.cleaned_data.get('email'), user = user)
                mr.save()
            except:
                messages.info(request, 'Email Already Exits')
    else:
        form = MailReceiverModelForm()
    
    mailReceiverObj = MailReceiverModel.objects.filter(user = user)
    context = {
        'form' : form,
        'mailReceivers' : mailReceiverObj,
    }
    return render(request, 'profile.html', context)




def delReceiverView(Request, id):
    r = MailReceiverModel.objects.get(id = id)
    r.delete()
    messages.info(Request, 'E-Mail is Deleted!')
    return redirect('Users:profileView')