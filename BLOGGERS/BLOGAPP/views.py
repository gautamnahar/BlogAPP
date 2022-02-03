from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .models import Post, Category, Comment
from .forms import Postform, Editform, Commentform
from django.http import HttpResponseRedirect


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'BLOGAPP/home.html'
    # ordering = ['-id']
    ordering = ['-post_date']


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'BLOGAPP/articles_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = Postform
    template_name = 'BLOGAPP/add_post.html'
    # fields = '__all__'


class AddCommentView(CreateView):
    model = Comment
    form_class = Commentform
    template_name = 'BLOGAPP/add_comment.html'
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('home')


class AddCategoryView(CreateView):
    model = Category
    # form_class = Postform
    template_name = 'BLOGAPP/add_category.html'
    fields = '__all__'
    success_url = reverse_lazy('home')


class UpdatePostView(UpdateView):
    model = Post
    form_class = Editform
    template_name = 'BLOGAPP/update_post.html'
    # fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'BLOGAPP/delete_post.html'
    success_url = reverse_lazy('home')
