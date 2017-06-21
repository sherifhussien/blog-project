#(Queryset)
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post ,Comment
from blog.forms import PostForm,CommentForm
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.core.urlresolvers import reverse_lazy

# Create your views here.

class AboutView(TemplateView):
    template_name='blog/about.html' #to check blog/

class PostListView(ListView):
    context_object_name = 'posts'
    model= Post

    #allows me to use django's ORM when i dealing with generic views(sql query on my model)
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') #field condition:less than or equal

class PostDetailView(DetailView):
    context_object_name='post_detail'
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name= 'blog/post_detail.html'
    from_class=PostForm
    model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name= 'blog/post_detail.html'
    from_class=PostForm
    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    login_url='/login/'
    redirect_field_name= 'blog/post_detail.html'
    success_url=reverse_lazy('post_list')
    model=Post

class DraftListView(ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
