from django.conf.urls import patterns, url

from blog.views import PostsListView, PostsDetailView, PostByTagListView

urlpatterns = patterns('',
    url(r'^$', PostsListView.as_view(), name='post_list'),
    url(r'^(?P<pk>\d+)/$', PostsDetailView.as_view(), name='post_detail'),
    url(r'^bytag/(\w+)/$', PostByTagListView.as_view(), name='post_by_tag'),
)