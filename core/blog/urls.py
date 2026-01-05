from django.urls import path
from . import views

# APP NAME
app_name = "blog"

urlpatterns = [
    # Index page
    path('', views.index, name='index'),
    # CRUD operations for blog posts
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    path('posts', views.PostListView.as_view(), name='posts'),
    path('user/posts', views.user_posts, name='user-posts'),

    # Functional operations
    path("posts/<int:post_id>/submit_for_verification/", views.submit_post_for_verification, name="submit_post_for_verification"),
    path("posts/<int:post_id>/verify/", views.verify_post, name="verify_post"),
    path("posts/<int:post_id>/publish/", views.publish_post, name="publish_post"),
]

urlpatterns += [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin, name='admin'),
    path('dashboard/users/create', views.UserCreateView.as_view(), name='user-create'),
    path('dashboard/users/', views.UserListView.as_view(), name='user-list'),
    path('dashboard/users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user-update'),
    path('dashboard/users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('dashboard/users/<int:pk>/', views.UserProfileView.as_view(), name='user-profile'),
    path('dashboard/users/<int:user_id>/assign_to_group/',
    views.assign_user_to_group, name='assign_user_to_group'),
    # path('dashboard/users/<int:user_id>/assign_to_group/<str:group_name>/', views.assign_user_to_group, name='assign_user_to_group'),
    
    path('dashboard/groups/', views.GroupListView.as_view(), name='group-list'),
    path('dashboard/create/groups/', views.GroupCreateView.as_view(), name='group-create'),
    path('dashboard/<int:pk>/edit/', views.GroupUpdateView.as_view(), name='group-edit'),
    path('dashboard/<int:pk>/delete/', views.DeleteGroupView.as_view(), name='group-delete'),

]


urlpatterns += [
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('posts/<int:post_id>/comments/<int:pk>/edit_comment/', views.CommentUpdateView.as_view(), name='edit_comment'),
]