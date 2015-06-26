from django.conf.urls import patterns, include, url
# from django.contrib import admin
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from main.views import PostService

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^opensooq/', DjangoView.as_view(
    services=[PostService], tns='opensooq.webservice',
    in_protocol=Soap11(validator='lxml'), out_protocol=Soap11()), name="soap"),
    url(r'^search/(\w+)', 'main.views.search_post'),
    url(r'^delete/(\w+)', 'main.views.delete_post'),
    url(r'^add/(\w+)/(\w+)/(\w+)', 'main.views.add_post'),
    url(r'^update/(\w+)/(\w+)/(\w+)/(\w+)', 'main.views.update_post'),
    url(r'^list/', 'main.views.list_post'),

    # url(r'^admin/', include(admin.site.urls)),
)
