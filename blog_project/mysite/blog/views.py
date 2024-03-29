#(Queryset)
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from blog.models import Post ,Comment
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm,CommentForm
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.core.urlresolvers import reverse_lazy

# Create your views here.

class AboutView(TemplateView):
    template_name='blog/about.html' #to check blog/

class PostListView(ListView):
    # context_object_name = 'posts'
    model= Post

    #allows me to use django's ORM when i dealing with generic views(sql query on my model)
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') #field condition:less than or equal

class PostDetailView(DetailView):
    # context_object_name='post_detail'
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name= 'blog/post_detail.html'
    form_class=PostForm  #instead of fields=('author','text')
    model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    success_url=reverse_lazy('post_list')
    model=Post

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'comment_form.html',{'form':form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)#sends another request to the given url.

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
