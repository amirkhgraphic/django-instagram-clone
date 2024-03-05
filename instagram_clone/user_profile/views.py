from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from content.models import Post
from user.models import Follower
from user_activity.models import Comment, PostLike
from user_profile.forms import UpdateUserForm, UpdateProfileForm
from user_profile.models import Profile

User = get_user_model()


def current_user_view(request, user_id):
    user = User.objects.get(id=user_id)
    if user == request.user:
        return redirect('profile:user_profile')
    context = {
        'title': user.user_name,
    }
    return render(request, 'user_profile/current_user.html', context=context)


def user_profile_details_view(request, user_id):
    if not request.user.is_authenticated:
        return redirect('user:log-in')
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(pk=user.profile.pk)
    followers_list = Follower.objects.filter(user=user).all()
    details = {
        'user_id': user.id,
        'profile_id': profile.id,
        'profile_pic': profile.image.url,
        'username': user.user_name,
        'bio': profile.bio,
        'posts': Post.objects.filter(user=request.user).all().count(),
        'followers': Follower.followers_count(user=user),
        'following': Follower.following_count(followed_by=user),
        'is_following': followers_list.filter(user=user, followed_by=request.user).exists()
    }
    return JsonResponse({'details': details})


def user_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('user:log-in')

    followers = Follower.objects.filter(user=request.user).all().count()
    following = Follower.objects.filter(followed_by=request.user).all().count()
    no_posts = Post.objects.filter(user=request.user).all().count()
    context = {
        'title': request.user.user_name,
        'following': following,
        'followers': followers,
        'no_posts': no_posts,
        'bio': request.user.profile.bio
    }
    return render(request, 'user_profile/profile.html', context=context)


def edit_profile_view(request, username):
    if not request.user.is_authenticated:
        return redirect('user:log-in')

    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile:user_profile')
        else:
            errors = {}
            for form in [u_form, p_form]:
                for field, error in form.errors.items():
                    errors[field] = error
            context = {
                'title': 'Edit Profile',
                'u_form': u_form,
                'p_form': p_form,
                'errors': errors
            }
            return render(request, 'user_profile/edit_profile.html', context=context)

    u_form = UpdateUserForm(instance=request.user)
    p_form = UpdateProfileForm(instance=request.user.profile)
    context = {
        'title': 'Edit Profile',
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user_profile/edit_profile.html', context=context)


def follow_unfollow_view(request):
    user = User.objects.get(pk=request.POST['user_id'])
    followers_list = Follower.objects.filter(user=user).all()
    is_following = followers_list.filter(user=user, followed_by=request.user)

    if is_following.exists():
        is_following.delete()
        followers = Follower.objects.filter(user=user).all().count()
        return JsonResponse({'follow': False, 'followers': followers})

    else:
        Follower.objects.create(user=user, followed_by=request.user)
        followers = Follower.objects.filter(user=user).all().count()
        return JsonResponse({'follow': True, 'followers': followers})


def get_search_users_view(request):
    data = []
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.GET['username']
        users = User.objects.filter(user_name__icontains=username)
        for user in users:
            item = {
                'id': user.id,
                'username': user.user_name,
                'profile_pic': user.profile.image.url
            }
            data.append(item)
    return JsonResponse({'data': data[:10]})


def search_view(request):
    return render(request, 'user_profile/search.html', context={'title': 'Search'})


def get_user_posts_view(request, num_posts):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        visible = 10
        lower = num_posts - visible
        upper = num_posts
        posts = Post.objects.filter(user=request.user).all()
        data = []
        for post in posts:
            item = {
                'id': post.id,
                'author': post.user.user_name,
                'user_img': post.user.profile.image.url,
                'img': [{'url': media.media.url, 'type': media.type} for media in post.post_files.all()],
                'liked': PostLike.objects.filter(post=post, user=request.user).exists(),
                'likes': post.post_likes.count(),
                'content': post.caption,
                'created': post.time_diff,
                'no_of_comments': Comment.objects.filter(post=post).all().count()
            }
            data.append(item)
        return JsonResponse({'data': data[lower:upper], 'length': Post.objects.filter(user=request.user).all().count()})
