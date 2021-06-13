from django.shortcuts import redirect
from django.http import HttpResponse

def authenticatedUser(function):
    def wrapperFunction(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('Users:loginView')
    return wrapperFunction