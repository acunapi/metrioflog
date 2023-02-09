from django.http import JsonResponse
from ..models import *

def routes(request):
    routes = [
        'GET /api/posts',
        'GET /api/post/:id',
    ]
    return JsonResponse(routes, safe=False)

def posts(request):
    posts = Post.objects.all()
    posts_dict = []
    for p in posts:
        posts_dict.append({
            'total_likes' : p.total_likes,
            'content' : p.content
        })
    return JsonResponse(posts_dict, safe=False)

#NO FUNCIONA EL DEF POST
def post(request, id):
    post = Post.objects.get(id=id)
    post_dict = {
            'total_likes' : p.total_likes,
            'content' : p.content,
            'id' : p.id
        }
    return JsonResponse(post_dict, safe=False)