from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.PostListView.as_view(), name='posts'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('user/posts', views.user_posts, name='user-posts'),
]


urlpatterns += [
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    # path('posts/<int:post_id>/comments/<int:pk>/edit_comment/', views.CommentUpdateView.as_view(), name='edit_comment'),
]