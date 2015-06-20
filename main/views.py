# encoding: utf8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from django.db.models import Q

from spyne.model.primitive import Unicode
from spyne.model.complex import Iterable
from spyne.service import ServiceBase
from spyne.decorator import rpc
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.
from main.models import Post


@login_required
def home(request):
    return render(request, "home.html")


class PostService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Iterable(Unicode))
    def AddPost(ctx, username, password, title, description, post_type):
        if username == "root" and password == "F0T349M3RTo2":
            if title != "":
                new_post = Post.objects.create(title=title, description=description, type=post_type)
                yield {"post_id": str(new_post.id)}
                yield {"post_title": new_post.title}
                yield {"post_description": new_post.description}
                yield {"post_type": new_post.type}
            else:
                yield "post title is required"
        else:
            yield "401 authentication failed"

    @rpc(Unicode, Unicode, Unicode, _returns=Iterable(Unicode))
    def DeletePost(ctx, username, password, post_id):
        if username == "root" and password == "F0T349M3RTo2":
            if post_id != "":
                try:
                    new_post = Post.objects.get(pk=post_id)
                    new_post.delete()
                    yield "post has been deleted"
                except:
                    yield "no post with such ID"
            else:
                yield "post id is required"
        else:
            yield "401 authentication failed"

    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Iterable(Unicode))
    def UpdatePost(ctx, username, password, post_id, title, description, post_type):
        if username == "root" and password == "F0T349M3RTo2":
            if post_id != "" and title != "":
                try:
                    new_post = Post.objects.get(pk=post_id)
                    new_post.title = title
                    new_post.description = description
                    new_post.type = post_type
                    new_post.save()
                    yield "post has been edited"
                    yield {"post_id": str(new_post.id)}
                    yield {"post_title": new_post.title}
                    yield {"post_description": new_post.description}
                    yield {"post_type": new_post.type}
                except:
                    yield "no post with such ID"
            elif post_id == "":
                yield "post id is required"
            elif title == "":
                yield "title is required"
        else:
            yield "401 authentication failed"

    @rpc(Unicode, _returns=Iterable(Unicode))
    def SearchPost(ctx, term):
        if term != "":
            new_post = Post.es.search(term)
            if not new_post:
                yield "There are no results that match your search"
            else:
                # yield new_post.es.serialize()
                for post in new_post.model.objects.all():
                    yield str(post.id)
                    yield post.title
                    yield post.description
                    yield post.type
        else:
            yield "please write your search term"

    @rpc(_returns=Iterable(Unicode))
    def ListPost(ctx):
        posts = Post.es.all()
        if not posts:
            yield "There are no posts yet"
        else:
            for post in posts.model.objects.all():
                yield str(post.id)
                yield post.title
                yield post.description
                yield post.type


def search_post(request, term):
    new_post = Post.es.search(term)
    return HttpResponse(new_post)


def list_post(request):
    new_post = Post.es.all()
    return HttpResponse(new_post)


@login_required
def add_post(request, title, description, type):
    new_post = Post.objects.create(title=title, description=description, type=type)
    new_post = Post.es.get(pk=new_post.id)
    new_post['status'] = "post has been added successfully"
    return JsonResponse(new_post)


@login_required
def update_post(request, post_id, title, description, type):
    try:
        post = Post.objects.get(pk = post_id)
    except:
        response = {}
        response['status'] = "no post with such id"
        return JsonResponse(response)
    post.title = title
    post.description = description
    post.type = type
    post.save()
    new_post = Post.es.get(pk=post.id)
    new_post['status'] = "post has been updated successfully"
    return JsonResponse(new_post)


@login_required
def delete_post(request, id):
    try:
        new_post = Post.objects.get(pk=id)
        new_post.delete()
        response = {}
        response['status'] = "post has been deleted successfully"
    except:
        response = {}
        response['status'] = "no post with such id"
    return JsonResponse(response)