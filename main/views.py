# main/views.py
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from .models import BlogPost

def blog_page(request):
    return render(request, 'index.html')

def get_posts(request):
    if request.method == 'GET':
        posts = BlogPost.objects.all().order_by('-id')
        return JsonResponse({'posts': [post.to_dict() for post in posts]})
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def blog_crud(request):
    if request.method == 'POST':
        # Create
        data = json.loads(request.body)
        post = BlogPost.objects.create(title=data['title'], content=data['content'])
        return JsonResponse(post.to_dict(), status=201)

    elif request.method == 'PUT':
        # Update
        data = json.loads(request.body)
        try:
            post = BlogPost.objects.get(id=data['id'])
            post.title = data['title']
            post.content = data['content']
            post.save()
            return JsonResponse(post.to_dict())
        except BlogPost.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

    elif request.method == 'DELETE':
        # Delete
        data = json.loads(request.body)
        try:
            post = BlogPost.objects.get(id=data['id'])
            post.delete()
            return JsonResponse({'deleted': True})
        except BlogPost.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

    return HttpResponseNotAllowed(['POST', 'PUT', 'DELETE'])
