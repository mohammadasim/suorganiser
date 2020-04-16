from django.shortcuts import redirect


def redirect(request):
    return redirect('blogs_posts_list')
