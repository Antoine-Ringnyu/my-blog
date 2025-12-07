from django.shortcuts import render
from .models import Post
from django.views import generic
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    # get all the posts
    
    # paginate_by = 1  # Number of posts per page
    posts = Post.objects.all().filter(status='published').order_by('-created_at')

    paginator = Paginator(posts, 10)  # Show 1 post per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # create context dictionary to pass to template
    context = {
        'page_obj': page_obj,
        # 'paginate_by': paginate_by
    }


    return render(request, 'blog/index.html', context)


# ###############################################################
# POST 
# ###############################################################
class PostListView(generic.ListView):
    model = Post
    # template_name = 'blog/post_list.html' # Specify your own template name/location
    context_object_name = 'posts'  # your own name for the list as a template variable
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-created_at')
    
class PostDetailView(generic.DetailView):
    model = Post
    # template_name = 'blog/post_detail.html' # Specify your own template name/location
    context_object_name = 'post'  # your own name for the object as a template variable