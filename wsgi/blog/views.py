from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


def index(request):
        return render(request, 'index.html')


def post_list(request):
        # filter unpublished posts
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, slug):
        post = get_object_or_404(Post, slug=slug)
        projects_length = len(post.project.all())
        form = CommentForm(request.POST or None)
        if form.is_valid():
                print(request.user.email)
                comment = form.save(commit=False)
                comment.author = request.user.get_full_name()
                comment.post = post
                comment.save()
                return redirect(request.path)
        return render(request, 'blog/post_detail.html', {'post': post, 'projects_length': projects_length, 'form': form})


@login_required
def post_new(request):
        if request.method == 'POST':
                form = PostForm(request.POST)
                if form.is_valid():
                        post = form.save(commit=False)
                        post.author = request.user
                        post.save()
                        # This saves the project relation
                        form.save_m2m()
                        return redirect('blog.views.post_detail', slug=post.slug)
        else:
                form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.method == "POST":
                form = PostForm(request.POST, instance=post)
                if form.is_valid():
                        post = form.save(commit=False)
                        post.author = request.user
                        post.save()
                        # This saves project relation
                        form.save_m2m()
                return redirect('blog.views.post_detail', slug=post.slug)
        else:
                action = "Edit"
                form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form, 'action': action})


@login_required
def post_draft_list(request):
        posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
        return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.publish()
        return redirect('blog.views.post_detail', slug=slug)


@login_required
def post_delete(request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        return redirect('blog.views.post_list')
