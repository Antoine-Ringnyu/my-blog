from django.shortcuts import render
from .models import Post
from django.views import generic

# Create your views here.

def index(request):
    # get all the posts
    
    posts = Post.objects.all().filter(status='published').order_by('-created_at')

    # # get the comments for each post
    # for post in posts:
    #     post.comments_list = post.comments.all().order_by('-created_at')
    # template location: core/blog/templates/blog/index.html

    return render(request, 'blog/index.html', {'posts': posts})

# ###############################################################
# POST 
# ###############################################################
class PostListView(generic.ListView):
    model = Post
    # template_name = 'blog/post_list.html' # Specify your own template name/location
    context_object_name = 'posts'  # your own name for the list as a template variable
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-created_at')
    
class PostDetailView(generic.DetailView):
    model = Post
    # template_name = 'blog/post_detail.html' # Specify your own template name/location
    context_object_name = 'post'  # your own name for the object as a template variable