from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import AnakForm
from django.contrib import messages
# Create your views here.
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import CreateUserForm,accountForm
from django.contrib.auth.models import Group
from .models import Anak
from django.contrib.auth import authenticate, login, logout

from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save()
            # user = form.cleaned_data.get('username')
            username = form.cleaned_data.get('username')

            # dibawah di komen karna di piindah ke signals untuk buat profileny
            # jadi jika kita register ke sini otomatis kita langsung jadi customer dan di tambahkan
            groub = Group.objects.get(name='murid')
            user.groups.add(groub)
            # ini agar pada saat kita login kita akan otomatis login sebagai user atau customer
            Anak.objects.create(
                user=user,
                nama=user.username,
                )
            # messages.success(request,'Account was created for ' + user)
            messages.success(request,'Account was created for ' + username)
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form':form}
    return render(request, 'account/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'password dan usernamemu salah cuy')
    context = {}
    return render(request,'account/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    anak = Anak.objects.all()
    anak = Anak.objects.all().order_by('-tanggal_antar')
    jumlah = anak.count()
    pending = anak.filter(status='Masih Cuci').count()
    selesai = anak.filter(status='Selesai').count()
    kosong = anak.filter(status='Kosong').count()
    paginator = Paginator(anak,10)
    page = request.GET.get('page')
    try:
        anak = paginator.page(page)
    except PageNotAnInteger:
        anak = paginator.page(1)
    except EmptyPage:
        anak = paginator.page(paginator.num_pages)


    context = {
        'anak':anak,
        'pending': pending,
        'selesai': selesai,
        'kosong': kosong,
        'jumlah':jumlah
    }
    return render(request,'account/home.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['murid'])
def dashboard(request):
    murid = Anak.objects.all()
    pending = murid.filter(status='Masih Cuci').count()
    selesai = murid.filter(status='Selesai').count()

    keren = request.user.anak
    context = {
        'user':murid,
        'pending': pending,
        'selesai': selesai,
        'anak':keren,
    }
    return render(request,'account/dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['murid'])
def accountSettings(request):
    anak = request.user.anak
    form = accountForm(instance=anak)

    if request.method == 'POST':
        form = accountForm(request.POST,request.FILES,instance=anak)
        if form.is_valid:
            form.save()

    context = {'form': form}
    return render(request,'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['pencuci'])
def createAnak(request):
    anak = Anak.objects.all().order_by('-tanggal_antar')
    jumlah = anak.count()
    pending = anak.filter(status='Masih Cuci').count()
    selesai = anak.filter(status='Selesai').count()
    kosong = anak.filter(status='Kosong').count()
    form = AnakForm()
    if request.method == 'POST':
        form = AnakForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('nama')
            messages.success(request,f'Si {username} berhasil di tambahkan cuyy')
            return HttpResponseRedirect('/')
    else:
        AnakForm()
    context = {
        'form':form,
        'anak':anak,
        'pending': pending,
        'selesai': selesai,
        'kosong': kosong,

    }
    return render(request,'account/createanak.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['pencuci'])
def deleteAnak(request,pk):
    anak_to_delete = Anak.objects.get(id=pk)
    anak = Anak.objects.all().order_by('-tanggal_antar')
    jumlah = anak.count()
    pending = anak.filter(status='Masih Cuci').count()
    selesai = anak.filter(status='Selesai').count()
    kosong = anak.filter(status='Kosong').count()
    if request.method == 'POST':
        anak_to_delete.delete()

        messages.warning(request,'Sudah terhapus Cuyyy')
        return redirect('/')
    context = { 
        'anak_to_delete':anak_to_delete,
        'anak':anak,
        'pending': pending,
        'selesai': selesai,
        'kosong': kosong,
    }
    return render(request,'account/delete.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['pencuci'])
def updateAnak(request,pk):
    anak_update = Anak.objects.get(id=pk)
    anak = Anak.objects.all().order_by('-tanggal_antar')
    jumlah = anak.count()
    pending = anak.filter(status='Masih Cuci').count()
    selesai = anak.filter(status='Selesai').count()
    kosong = anak.filter(status='Kosong').count()
    form = AnakForm(instance=anak_update)
    if request.method == 'POST':
        form = AnakForm(request.POST,instance=anak_update)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {
        'form': form,
        'anak':anak,
        'pending': pending,
        'selesai': selesai,
        'kosong': kosong,
    }
    return render(request,'account/update.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['pencuci'])
def detailAnak_pending(request):
    anak = Anak.objects.filter(status='Masih Cuci')
    context = {
        'anak': anak,
    }
    return render(request,'account/detail.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['pencuci'])
def detailAnak_kosong(request):
    anak = Anak.objects.filter(status='Kosong')
    context = {
        'anak': anak,

    }
    return render(request,'account/detail_kosong.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['pencuci'])
def detailAnak_selesai(request):
    anak = Anak.objects.filter(status='Selesai')
    context = {
        'anak': anak,
    }
    return render(request,'account/detail_selesai.html',context)
