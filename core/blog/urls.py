from django.urls import path
from . import views

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
    path("posts/<int:post_id>/verify/", views.verify_post, name="verify_post"),
]

urlpatterns += [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/groups/', views.GroupListView.as_view(), name='group-list'),
    path('dashboard/create/groups/', views.GroupCreateView.as_view(), name='group-create'),
    path('dashboard/<int:pk>/edit/', views.GroupUpdateView.as_view(), name='group-edit'),
    path('dashboard/<int:pk>/delete/', views.DeleteGroupView.as_view(), name='group-delete'),

]


urlpatterns += [
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('posts/<int:post_id>/comments/<int:pk>/edit_comment/', views.CommentUpdateView.as_view(), name='edit_comment'),
]