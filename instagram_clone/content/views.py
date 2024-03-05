from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from content.forms import NewPostForm
from content.models import Post, PostMedia
from log.models import Log
from user_activity.models import Comment, PostLike


def get_posts(request, num_posts):
    if not request.user.is_authenticated:
        return redirect('user:login')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        visible = 10
        lower = num_posts - visible
        upper = num_posts
        posts = Post.objects.all()
        data = []
        for post in posts:
            item = {
                'id': post.id,
                'author_id': post.user.id,
                'author': post.user.user_name,
                'user_img': post.user.profile.image.url,
                'img': [{'url': media.media.url, 'type': media.type} for media in post.post_files.all()],
                'liked': post.post_likes.filter(user=request.user).exists(),
                'likes': post.post_likes.count(),
                'content': post.caption,
                'created': post.time_diff,
                'no_of_comments': Comment.objects.filter(post=post).all().count()
            }
            data.append(item)
        return JsonResponse({'data': data[lower:upper], 'length': Post.objects.all().count()})


def like_unlike_view(request):
    if not request.user.is_authenticated:
        return redirect('user:login')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        pk = request.POST.get('pk')
        post = Post.objects.get(id=pk)

        if PostLike.objects.filter(post=post, user=request.user).exists():
            post.post_likes.filter(user=request.user).delete()
            liked = True

        else:
            PostLike.objects.create(user=request.user, post=post)
            liked = False

        return JsonResponse({'liked': liked, 'count': PostLike.post_likes(pk).count()})


def post_delete_view(request, pk):
    post = Post.objects.get(pk=pk)
    if post.user != request.user:
        return redirect('home')
    post.delete()
    messages.success(request, 'Your post has been deleted successfully!')
    return redirect('home')


def comment_view(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        pk = request.POST.get('pk')
        comment_data = request.POST.get('commentData')
        post = Post.objects.get(id=pk)
        comment = Comment(content=comment_data, author=request.user, post=post)
        comment.save()
        commented = True
        return JsonResponse({'commented': commented, 'no_of_comments': post.comments.count(), 'user_id': request.user.id, 'user_name': request.user.user_name, 'profile_pic': request.user.profile.image.url, 'time': '0 seconds ago', 'comment_content': comment_data})


def new_post(request):
    if not request.user.is_authenticated:
        return redirect('user:login')
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            media_files = request.FILES.getlist('media_files')
            for media_file in media_files:
                PostMedia.objects.create(post=post, media=media_file, type=request.POST['media_type'])

            messages.success(request, 'New Post has been posted')
            return redirect('home')
    else:
        form = NewPostForm()

    context = {
        'title': 'New Post',
        'is_form': 2,
        'form': form
    }
    return render(request, 'content/new_post.html', context=context)


def current_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        'title': 'Post',
        'post': post,
        'profile_pic_url': post.user.profile.image.url,
        'user_name': post.user.user_name,
        'post_img': [{'url': media.media.url, 'type': media.type} for media in post.post_files.all()],
    }
    Log.objects.create(operation='READ', action=f'{request.user.user_name} with user-id {request.user.id} has watched post with post-id {post_id}')
    return render(request, 'content/current_post.html', context=context)


def get_post_comments(request, pk):
    comments = Comment.objects.filter(post__id=pk).all()
    data = []
    for comment in comments:
        item = {
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.user_name,
            'time': comment.time_diff,
            'author_id': comment.author.id,
            'author_profile_pic': comment.author.profile.image.url
        }
        data.append(item)
    return JsonResponse({'data': data})


def get_post_details(request, pk):
    post = Post.objects.get(pk=pk)
    # comments = Comment.objects.filter(post=post).all()
    # comment_list = []
    data = {
        'id': post.id,
        'author_id': post.user.id,
        'author': post.user.user_name,
        'user_img': post.user.profile.image.url,
        'img': [{'url': media.media.url, 'type': media.type} for media in post.post_files.all()],
        'liked': post.post_likes.filter(user=request.user).exists(),
        'likes': post.post_likes.count(),
        'content': post.caption,
        'created': post.time_diff,
        'no_of_comments': Comment.post_comments(post.id).count(),
        'is_author': post.user == request.user
    }
    return JsonResponse({'data': data})


def post_update_view(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('home')
    form = NewPostForm(instance=post)
    context = {
        'title': 'Update Post',
        'is_form': 1,
        'form': form
    }
    return render(request, 'content/new_post.html', context=context)
