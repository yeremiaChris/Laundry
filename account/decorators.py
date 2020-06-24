from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args,**kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):

            groub = None
            # jadi dibawah ini jika useritu bagian dari groub
            if request.user.groups.exists():
            # jadi indeks 0 itu adlah yang pertama ada di lists
                groub = request.user.groups.all()[0].name

            # jika groub itu ada di allowed_roles list jika ada namany
            if groub in allowed_roles:
                # return di bawah ini adalah jika groub itu aadalah admin return funct dibawah
                return view_func(request, *args,**kwargs)
            else:
                return HttpResponse('you are not authorized to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args,**kwargs):
        groub = None
        if request.user.groups.exists():
            groub = request.user.groups.all()[0].name
        if groub == 'murid':
            return redirect('user-page')
        if groub == 'pencuci':
            return view_func(request, *args,**kwargs)

    return wrapper_func
