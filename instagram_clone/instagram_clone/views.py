from django.shortcuts import redirect, render

from content.models import Post


def home(request):
    if not request.user.is_authenticated:
        return redirect('user:log-in')
    posts = Post.objects.all()
    context = {
        'title': 'Home'
    }
    return render(request, 'home.html', context=context)