from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from .models import Post, Comment
from .forms import CommentForm
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required



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

    # additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    
    context_object_name = 'post'  # your own name for the object as a template variable


# user posts
@login_required
@permission_required('blog.change_post', raise_exception=True)
def user_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')

    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'blog/user_posts.html', context)




# ################################################################
# COMMENTS SECTION
# ################################################################

# Add comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm

@login_required
def add_comment(request, post_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect(
        post.get_absolute_url()
    )


# update commment (generic view)
# class CommentUpdateView(generic.UpdateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'blog/post_detail.html'

#     def get_success_url(self):
#         return self.object.post.get_absolute_url()