from multiprocessing import context
from urllib import response
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from .forms import CommentForm, CustomLoginForm, GroupForm, PostForm
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required



# Create your views here.

def index(request):
    # get all the posts
    
    # paginate_by = 1  # Number of posts per page
    posts = Post.objects.filter(
        status='published',
        verified=True,
    ).order_by('-created_at')


    paginator = Paginator(posts, 3)  # Show 1 post per page
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
    # template_name = 'blog/post.html' # Specify your own template name/location

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

from django.contrib.auth.mixins import LoginRequiredMixin
class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    # template_name = 'blog/post_form.html'
    redirect_field_name = 'next'     # Keeps track of where to return after login
    success_url = reverse_lazy('dashboard')
    

    #  redirect to next if available
    # def get_success_url(self):
    #     return self.request.POST.get('next') or self.request.GET.get('next') or 'dashboard' 


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    # template_name = 'blog/post_form.html'
    success_url = reverse_lazy('dashboard')

    # redirect to next if available
    # def get_success_url(self):
        # return self.request.POST.get('next') or self.request.GET.get('next') or 'dashboard'

    # check if the user is the author of the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView( generic.DeleteView):
    model = Post
    # template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('dashboard')  # Redirect to home page after deletion
    # def get_success_url(self):
    #     return self.request.POST.get('next') or self.request.GET.get('next') or 'dashboard'

    def form_invalid(self, form):
        try:
            self.object.delete()
            return redirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('post-delete', kwargs={'pk': self.object.pk})
            )


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect

# Only admin or staff can verify
@user_passes_test(lambda u: u.is_staff)
def verify_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.set_as_verified()
    return redirect(post.get_absolute_url())



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


# ##########################################################
# LOGIN VIEW WITH CUSTOM FORM
# ##########################################################

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm



# ##########################################################
# DASHBOARD VIEW
# ##########################################################
from django.contrib.admin.views.decorators import staff_member_required 
# @staff_member_required
@login_required
def dashboard(request):
    # get all the users posts
    posts = Post.objects.all().order_by('-created_at')

    # get all groups
    groups = Group.objects.all()
    
    total_posts = Post.objects.count()
    # total_comments = Comment.objects.count()
    verified_posts = Post.objects.filter(verified=True).count()
    draft_posts = Post.objects.filter(status='draft').count()
    published_posts = Post.objects.filter(status='published').count()

    context = {
        'posts': posts,
        'total_posts': total_posts,
        # 'total_comments': total_comments,
        'verified_posts': verified_posts,
        'draft_posts': draft_posts,
        'published_posts': published_posts,
        'groups' : groups
        
    }

    return render(request, 'blog/dashboard.html', context)



# ##########################################################
# GROUPS AND PERMISSIONS VIEW
# ##########################################################
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def setup_groups_and_permissions():
    # Create groups
    admin_group, created = Group.objects.get_or_create(name='Admin')
    editor_group, created = Group.objects.get_or_create(name='Editor')
    viewer_group, created = Group.objects.get_or_create(name='Viewer')

    # Get content type for Post model
    post_content_type = ContentType.objects.get_for_model(Post)

    # Define permissions
    can_add_post = Permission.objects.get(codename='add_post', content_type=post_content_type)
    can_change_post = Permission.objects.get(codename='change_post', content_type=post_content_type)
    can_delete_post = Permission.objects.get(codename='delete_post', content_type=post_content_type)
    can_view_post = Permission.objects.get(codename='view_post', content_type=post_content_type)
    can_verify_post = Permission.objects.get(codename='can_verify_post', content_type=post_content_type)

    # Assign permissions to groups
    admin_group.permissions.set([can_add_post, can_change_post, can_delete_post, can_view_post, can_verify_post])
    editor_group.permissions.set([can_add_post, can_change_post, can_view_post])
    viewer_group.permissions.set([can_view_post])

# Call the setup function (you might want to call this from a management command or an admin view)
# setup_groups_and_permissions()

class GroupListView(generic.ListView):
    model = Group
    template_name = 'blog/group_list.html'
    context_object_name = 'groups'

from django.contrib.auth.models import Group, Permission
from django.views import generic
from django.urls import reverse_lazy
from collections import defaultdict

class GroupCreateView(generic.CreateView):
    model = Group
    template_name = 'blog/group_form.html'
    form_class = GroupForm
    success_url = reverse_lazy('group-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        permissions = Permission.objects.select_related("content_type")

        grouped_permissions = defaultdict(list)

        for perm in permissions:
            key = (
                perm.content_type.app_label,
                perm.content_type.model
            )
            grouped_permissions[key].append(perm)

        context["grouped_permissions"] = grouped_permissions
        return context




class GroupUpdateView(generic.UpdateView):
    model = Group
    template_name = 'blog/group_form.html'
    form_class = GroupForm
    success_url = reverse_lazy('group-list')

class DeleteGroupView(generic.DeleteView):
    model = Group
    template_name = 'blog/group_confirm_delete.html'
    success_url = reverse_lazy('group-list')  # Redirect to home page after deletion