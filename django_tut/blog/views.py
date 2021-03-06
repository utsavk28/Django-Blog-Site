from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post

# Create your views here.


def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'title': 'Hello'
    }
    return render(request,  'blog/home.html', context)

# <app>/<model>_<viewtype>.html


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)
