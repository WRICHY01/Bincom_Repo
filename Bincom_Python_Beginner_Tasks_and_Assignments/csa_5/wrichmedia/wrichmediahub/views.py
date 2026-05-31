from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Post, MediaItem
from .forms import PostForm, MediaItemFormSet

# Create your views here.
def home_view(request):
    # return HttpResponse("Hello, World!")
    posts = Post.objects.all().prefetch_related("media_items", "author")
    return render(request, "wrichmediahub/home.html", {"posts": posts})


@login_required
def create_post_view(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        formset = MediaItemFormSet(
            request.POST,
            request.FILES
        )

        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            formset.instance = post
            formset.save()

            messages.success(request, "Post created successfully!")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        post_form = PostForm()
        formset = MediaItemFormSet()

    return render(request, "wrichmediahub/create_post.html", {
        "post_form": post_form,
        "formset": formset
    })

def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    media_items = post.media_items.all()
    return render(request, "wrichmediahub/post_detail.html", {
        "post": post,
        "media_items": media_items
    })

@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, "You can only delete your own posts")
        return redirect("home")
    
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("home")
    
    return render(request, "wrichmediahub/confirm_delete.html", {"post", post})