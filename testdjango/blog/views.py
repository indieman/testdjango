__author__ = 'indieman'

from django.views.generic import ListView, DetailView

from blog.models import Post, Hashtag


class PostsListView(ListView):
    model = Post
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        context['hashtags'] = Hashtag.objects.all()
        return context


class PostByTagListView(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        hashtag = Hashtag.objects.filter(name='%s' % self.args[0])
        return Post.objects.filter(hashtags=hashtag).all()

    def get_context_data(self, **kwargs):
        context = super(PostByTagListView, self).get_context_data(**kwargs)
        context['hashtags'] = Hashtag.objects.all()
        return context


class PostsDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostsDetailView, self).get_context_data(**kwargs)
        context['hashtags'] = Hashtag.objects.all()
        return context