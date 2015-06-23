# encoding: utf8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from spyne.model.primitive import Unicode
from spyne.model.complex import Iterable
from spyne.service import ServiceBase
from spyne.decorator import rpc
from django.http import HttpResponse, JsonResponse
from main.models import Post
from elasticsearch import Elasticsearch


# Create your views here.
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
            es = Elasticsearch()
            result = es.search(index="my-posts", q=term)
            if not result["hits"]["hits"]:
                yield "There are no results that match your search"
            else:
                hits = []
                # yield new_post.es.serialize()
                for hit in result["hits"]["hits"]:
                    dic = {}
                    dic["id"] = hit["_id"]
                    dic["score"] = str(hit["_score"])
                    dic["title"] = hit["_source"]["title"]
                    dic["description"] = hit["_source"]["description"]
                    dic["type"] = hit["_source"]["type"]
                    hits.append(dic)
                yield str(hits).strip('[]')
        else:
            yield "please write your search term"

    @rpc(_returns=Iterable(Unicode))
    def ListPost(ctx):
        es = Elasticsearch()
        result = es.search(index="my-posts", body={"query": {"match_all": {}}})
        if not result["hits"]["hits"]:
            yield "There are no posts yet"
        else:
            hits = []
            for hit in result["hits"]["hits"]:
                dic = {}
                dic["id"] = hit["_id"]
                dic["score"] = str(hit["_score"])
                dic["title"] = hit["_source"]["title"]
                dic["description"] = hit["_source"]["description"]
                dic["type"] = hit["_source"]["type"]
                hits.append(dic)
            yield str(hits).strip('[]')


def search_post(request, term):
    es = Elasticsearch()
    result = es.search(index="my-posts", q=term)
    return JsonResponse(result)


def list_post(request):
    es = Elasticsearch()
    result = es.search(index="my-posts", body={"query": {"match_all": {}}})
    return JsonResponse(result)


@login_required
def add_post(request, title, description, type):
    new_post = Post.objects.create(title=title, description=description, type=type)
    es = Elasticsearch()
    post = es.index(index="my-posts", doc_type="demo", id=new_post.id,
                    body={"title": new_post.title, "description": new_post.description, "type": new_post.type})
    return JsonResponse(post)


@login_required
def update_post(request, post_id, title, description, type):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        response = {}
        response['status'] = "no post with such id"
        return JsonResponse(response)
    post.title = title
    post.description = description
    post.type = type
    post.save()
    es = Elasticsearch()
    new_post = es.get(index="my-posts", doc_type='demo', id=post.id)
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