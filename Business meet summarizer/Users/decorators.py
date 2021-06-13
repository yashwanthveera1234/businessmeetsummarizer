from django.shortcuts import redirect

def authenticatedUser(function):
    def wrapperFunction(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('Users:loginView')
    return wrapperFunction

def unAuthenticatedUser(function):
    def wrapperFunction(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Users:homeView')
        else:
            return function(request, *args, **kwargs)
    return wrapperFunction