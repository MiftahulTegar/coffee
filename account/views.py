from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from .models import Comment, UserProfileInfo, Kategori, Produk
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm, UserProfileInfoForm, LoginForm, UserEditForm, UserEditProfile, CommentForm

def index(request):
    if request.user.is_authenticated:
        return render(request,'login/nav.html',{})
    return render(request,'akun/index.html')

def produk(request):
    a = Produk.published.all().filter(Kategori=1)
    b = Produk.published.all().filter(Kategori=2)
    c = Produk.published.all().filter(Kategori=3)
    return render(request,
                'menu/produk.html', 
                {'a':a, 'b':b, 'c':c, 'media_url':settings.MEDIA_URL})

def coffee(request):
    a = Produk.published.all().filter(Kategori=1)
    return render(request,
                'produk/coffee.html', 
                {'a':a, 'media_url':settings.MEDIA_URL})

def frappe(request):
    b = Produk.published.all().filter(Kategori=2)
    return render(request,
                'produk/frappe.html', 
                {'b':b, 'media_url':settings.MEDIA_URL})

def non_coffee(request):
    c = Produk.published.all().filter(Kategori=3)
    return render(request,
                'produk/non_coffee.html', 
                {'c':c, 'media_url':settings.MEDIA_URL})

def blog(request):
    object_list = Produk.published.all()
    paginator = Paginator(object_list, 8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                'menu/blog.html', 
                {'page': page, 'posts': posts})

def post_detail(request, post):
    post = get_object_or_404(Produk, slug=post, status='published')
    # menampilkan gambar berdasarkan nama
    img = Produk.published.all().filter(slug=post, status='published')
    comments = post.blog_comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save() 
            
    else:
        comment_form = CommentForm()                    
    return render(request, 'menu/detail.html', 
                        {'post': post, 'img':img,
                        'comments': comments,
                        'new_comment': new_comment,
                        'comment_form': comment_form, 'media_url':settings.MEDIA_URL})

def pembelian(request):
    a = Produk.published.all()
    b = Kategori.objects.all()
    return render(request,
                'menu/pembelian.html', 
                {'a':a, 'b':b})

def profile(request):
    img = UserProfileInfo.objects.filter(user=request.user.id)
    return render(request,'login/profile.html',{'img':img, 'media_url':settings.MEDIA_URL})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = UserEditProfile(
                                instance=request.user.userprofileinfo,
                                data=request.POST,
                                files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                    'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserEditProfile(instance=request.user.userprofileinfo)
            
    return render(request,
                    'akun/edit.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Atur kata sandi yang dipilih
            user.set_password(user.password)
            # Simpan objek Pengguna
            user.save()
            # Buat objek pengguna baru tetapi hindari menyimpannya dulu
            profile = profile_form.save(commit=False)
            profile.user = user
            # Simpan objek Pengguna
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'akun/register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
    
@login_required
def dashboard(request):
    return render(request, 'login/nav.html', {'section': 'dashboard'})
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    form = "Dummy String"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else: 
        form = LoginForm()
    return render(request, 'akun/login.html', {'form':form})