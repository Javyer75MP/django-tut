from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView



#def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #return render(request, 'blog/post_list.html', {'posts' : posts})

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class PostList(ListView):
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return queryset


# def post_detail(request, pk):

#     post = get_object_or_404(Post, pk=pk)
#     comments = Comment.objects.filter(post=post).order_by('created_date')

#     if request.method == "POST":
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author =request.user
#             comment.post = post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()

#     return render(request, 'blog/post_detail.html', {'post' : post, 'comments' : comments, 'form' : form})



class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('created_date')
        context['forms'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            form = CommentForm(request.POST)
            post = self.get_object()
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author =request.user
                comment.post = post
                comment = save()

                return redirect('post_detail.html', pk=post.pk)
            else:

                return redirect('login')

            
# @login_required(login_url='login')
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)

#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author =request.user
#             post.publish() 
#             return redirect('blog.views.post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})


class PostCreate(CreateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'
   

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk })




# @login_required(login_url='login')
# def post_edit(request, pk):
#         post = get_object_or_404(Post, pk=pk)

#         if request.method == "POST":
#             form = PostForm(request.POST, instance=post)
#             if form.is_valid():
#                 post = form.save(commit=False)
#                 post.author = request.user
#                 post.save()
#                 return redirect('post_detail', pk=post.pk)
#         else:
#             form = PostForm(instance=post)
#         return render(request, 'blog/post_edit.html', {'form': form, 'post' : post})


class PostEdit(UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk })




# @login_required(login_url='login')
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#     return redirect('post_list')



class PostDelete(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('post_list')
    
