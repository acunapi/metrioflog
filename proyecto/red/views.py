from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm, ProfileImageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Se inició sesión correctamente')
                return redirect("/")

        messages.error(request, 'Datos incorrectos')

    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect("/")


def feed(request):
    posts = Post.objects.all()

    context = {'posts':posts}
    return render(request, 'feed.html', context)

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('/register')
        if not last_name:
            last_name = ''
        User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        messages.success(request, f'Usuario {username} se creó correctamente.')
        return redirect('/')
    return render(request, 'register.html')

def post(request):
    current_user = get_object_or_404(User,pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, 'Post enviado')
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'post.html', {'form' : form})

def post_edit(request, post_id):
    current_user = get_object_or_404(User,pk=request.user.pk)
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post actualizado')
            return redirect('/')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

def comment(request):
    post_id = request.POST.get('post', '')
    if not post_id:
        raise Http404("Post no encontrado")
    p = get_object_or_404(Post, id=post_id)
    Comment.objects.create(
        text = request.POST.get('text'),
        user = request.user,
        post = p
    )
    return redirect("/")


@login_required
def like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post')
        post = get_object_or_404(Post, id=post_id)
        like = Like(post=post, user=request.user)
        like.save()
        post.total_likes += 1
        post.save()
    return redirect('/')


def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request, 'profile.html', {'user':user, 'posts': posts})


def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationships(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'Sigues a {username}')
    return redirect('/')

def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationships.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Ya no sigues a {username}')
    return redirect('/')


@login_required
def upload_profile_image(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileImageForm(instance=profile)
    return render(request, 'upload_profile_image.html', {'form': form})
