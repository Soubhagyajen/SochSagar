from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm
from .forms import BlogPostForm, UserRegisterForm, CommentForm
from .models import BlogPost, Comment, Poll
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.

# Home page
def home(request):
    return render(request, 'layout.html')


# Create a blog post
@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)  # Don't save yet
            # if request.FILES.get('image'):
            #     blog_post.image = request.FILES['image'].read()
            blog_post.author = request.user  # Assign the logged-in user
            blog_post.save()  # Now save with the correct author
            return redirect("blog_list")  # Redirect after saving
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {"form": form})



def display_image(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if post.image:
        # Check the content type (adjust based on image type)
        content_type = "image/jpeg"  # Default
        if post.image.startswith(b'\x89PNG\r\n\x1a\n'):  # Check if PNG
            content_type = "image/png"
        return HttpResponse(post.image, content_type=content_type)
    return HttpResponse("No Image", content_type="text/plain")




# List all blog posts
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'post.html', {'posts': posts})


# Update a blog post
@login_required
def blog_update(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'create_post.html', {'form': form})


# Delete a blog post
@login_required
def delete_blog(request, id):
    blog = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'delete_blog.html', {"blog": blog})


# User registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = UserRegisterForm()
    return render(request, 'register/register.html', {'form': form})


# Blog detail view with comments
def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    comments = post.comments.all()

    # Increment views count
    post.views += 1
    post.save()

    # Handle comment form submission
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', id=id)  # ✅ Corrected redirect

    else:
        form = CommentForm()

    return render(request, 'blog_detail.html', {'post': post, 'comments': comments, 'form': form})


# Like a blog post
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # Remove the like
            liked = False
        else:
            post.likes.add(request.user)  # Add the like
            liked = True

        # Return the updated like count and liked status as JSON
        return JsonResponse({
            'likes': post.total_likes(),
            'liked': liked
        })
    return JsonResponse({'error': 'User not authenticated'}, status=401)

# Poll voting view
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == "POST":
        vote = request.POST.get("vote")
        if vote == "option1":
            poll.votes1 += 1
        elif vote == "option2":
            poll.votes2 += 1
        poll.save()
        return redirect('poll_result', poll_id=poll.id)

    return render(request, 'poll.html', {'poll': poll})

def search_posts(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    posts = BlogPost.objects.all()

    if query:
        # Filter posts by title (case insensitive)
        posts = posts.filter(title__icontains=query)

    return render(request, 'post.html', {'posts': posts})

def about(request):
    return render(request, 'about.html')