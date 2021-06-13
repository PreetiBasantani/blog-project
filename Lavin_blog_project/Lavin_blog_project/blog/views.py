from datetime import datetime

from django import template
from django.contrib.auth.models import User, Group
# from django.core.checks import register
from django.http import HttpResponseRedirect, request, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from blog.models import Post, Comment
from blog.forms import CommentForm, PostForm, UserForm
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
# from django_projects.Lavin_blog_project.Lavin_blog_project.blog.forms import CommentForm
# from django_projects.blog_project.Lavin_blog_project.Lavin_blog_project.blog.forms import UserForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list_page.html'


class PostCategoryListView(ListView):
    model = Post
    template_name = 'blog/post_list_page.html'

    def get_queryset(self):
        p = Post.objects.filter(category=self.kwargs['category'], published_on__isnull=False)
        return p


class PostDetailView(DetailView):
    model = Post
    form_class = CommentForm
    initial = {'author': 'Provide Author name', 'comment_text': 'Enter Comments here'}
    template_name = 'blog/post_detail_page.html'

    def get(self, request, *args, **kwargs):
        p_key = self.kwargs['pk']
        p = Post.objects.get(pk=p_key)
        print(p.comments.all())
        comment = self.form_class(initial=self.initial)
        # print(comment.author)
        return render(request, self.template_name, {'form': comment,
                                                    'post': p})


@login_required
def add_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print("post : ", post)
    if request.method == "POST":

        comment = CommentForm(request.POST)
        print("comment : ", comment)
        if comment.is_valid():
            print('valid data')
            # comment.save(commit=False)
            comment.author = request.POST['author']
            comment.comment_text = request.POST['comment_text']
            comment.post = post
            print(comment.post.id)
            # a= input(post)
            comment.save()
            print('done')
            return redirect('blog:post_detail', pk=post.pk)
        else:
            comment = CommentForm()
    return render(request, 'blog/post_detail_page.html', {'post': p, 'form': comment})


class InfoTemplateView(TemplateView):
    template_name = 'blog/about.html' \
                    ''

register = template.Library()


@register.filter('is_admin')
def is_admin(user):
    try:
        u = User.objects.get(username=user.username)
        admin_grp = Group.objects.get(name='Admin')
        return admin_grp in u.groups.all()
    except Group.DoesNotExist:
        return False


class PostCreateView(CreateView):
    model = Post
    # form_class = PostForm
    template_name = 'blog/create_post.html'
    fields = ['author', 'category', 'post_image', 'post_title', 'text']

    def get(self, request, *args, **kwargs):
        if is_admin(request.user):
            return super().get(request, *args, **kwargs)

        return HttpResponse("you don't have admin rights !!")


@user_passes_test(is_admin, login_url='/login/')
def draftview(request):
    draft_post = Post.objects.filter(published_on__isnull=True)
    return render(request, 'blog/draft_page.html', {'draft_list': draft_post})


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    fields = ['author', 'category', 'post_image', 'post_title', 'text']
    success_url = "/blog/success/"


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = "/blog/"


def success(request):
    context = {}
    msg = 'Post Updated Successfully !!!'
    context['success_msg'] = msg
    return render(request, 'blog/success.html', context)


def post_publish(request, pk):
    print('Got inside')
    post = get_object_or_404(Post, pk=pk)
    print('post', post)
    post.published_on = datetime.now()
    post.save()
    print('published updated')
    return HttpResponseRedirect(reverse('blog:post_list'))


def add_user(request):
    # admin_grp = Group.objects.get(name='admin')

    if request.method == 'POST':
        # if request.user.groups.filter(name=admin_grp):
        user = UserForm(request.POST)
        user.save()
        return HttpResponseRedirect('blog:login')
    # else:
    #        return HttpResponse("You don't have admin rights!!")
    # endif
    user = UserForm()
    return render(request, 'blog/add_user.html', {'form': user})

# class ThanksTemplateView(TemplateView):
#     comment_class = CommentForm
#     template_name = 'blog/post_detail_page.html'
#
#
#     def get(self, request, *args, **kwargs):
#         comment = self.comment_class()
#         return render(request, self.template_name, {'form': comment})
#
#     def post(self, request, *args, **kwargs):
#        # comment = self.comment_class(request.POST)
#        return HttpResponseRedirect('/post_detail/')
