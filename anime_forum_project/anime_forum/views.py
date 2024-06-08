from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Thread, Post, LogEntry
from .forms import ThreadForm, PostForm, UserRegisterForm, UserLoginForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.conf import settings
from django.core.cache import cache
from .serializers import ThreadSerializer
from rest_framework import generics

class ThreadListAPIView(generics.ListAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

class ThreadDetailAPIView(generics.RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


CACHE_TTL = 60 * 15  # 15 minutes



def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        next_url = request.POST.get('next', '/')
        response = redirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        activate(language)
        LogEntry.objects.create(user=request.user, action='CHANGE_LANGUAGE', details=f"Language changed to {language}")
        return response
    else:
        return redirect('/')

def category_list(request):
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()[:3]
        cache.set('categories', categories, CACHE_TTL)
    return render(request, 'anime_forum/category_list.html', {'categories': categories})


def all_categories(request):
    categoriesall = cache.get('all_categories')
    if not categoriesall:
        categoriesall = Category.objects.all()
        cache.set('all_categories', categoriesall, CACHE_TTL)
    return render(request, 'anime_forum/forums.html', {'categories': categoriesall})


def thread_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    threads = cache.get(f'threads_{category_id}')
    if not threads:
        threads = Thread.objects.filter(category=category)
        cache.set(f'threads_{category_id}', threads, CACHE_TTL)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.category = category
            thread.save()
            cache.delete(f'threads_{category_id}')  # Clear cache when a new thread is created
            return redirect('thread_list', category_id=category.id)
    else:
        form = ThreadForm()
    return render(request, 'anime_forum/thread_list.html', {'category': category, 'threads': threads, 'form': form})


def post_list(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = Post.objects.filter(thread=thread)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.thread = thread
            post.save()
            LogEntry.objects.create(user=request.user, action='CREATE_POST',details=f"Post created in thread '{thread.title}'")
            return redirect('post_list', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'anime_forum/post_list.html', {'thread': thread, 'posts': posts, 'form': form})


def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user = request.user
            thread.save()
            return redirect('thread_list', category_id=thread.category.id)
    else:
        form = ThreadForm()
    return render(request, 'anime_forum/create_thread.html', {'form': form})


def create_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.thread = thread
            post.save()
            return redirect('post_list', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'anime_forum/create_post.html', {'form': form, 'thread': thread})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user.email)  # Send welcome email
            login(request, user)
            LogEntry.objects.create(user=user, action='LOGIN', details='User registered and logged in')
            return redirect('category_list')
    else:
        form = UserRegisterForm()
    return render(request, 'anime_forum/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                LogEntry.objects.create(user=user, action='LOGIN', details='User logged in')
                return redirect('category_list')
    else:
        form = UserLoginForm()
    return render(request, 'anime_forum/login.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            LogEntry.objects.create(user=request.user, action='CREATE_POST', details=f"Post edited in thread '{post.thread.title}'")
            return redirect('post_list', thread_id=post.thread.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'anime_forum/edit_post.html', {'form': form, 'post': post})


@login_required
def logout_view(request):
    LogEntry.objects.create(user=request.user, action='LOGOUT', details='User logged out')
    logout(request)
    return redirect('category_list')


def send_welcome_email(user_email):
    subject = 'Welcome to Anime Forum'
    message = 'Thank you for registering at Anime Forum!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)
