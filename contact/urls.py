from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from . import views

urlpatterns = [
    path('post/', views.PostListView.as_view(), name='post_list'),
    path('userpost/', views.UserPostListView.as_view(), name='user_post_list'),
    path('userpost/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('userpost/new', views.PostCreateView.as_view(), name='post_new'),
    path('userpost/edit/<int:pk>', views.PostUpdateView.as_view(), name='post_form'),
    path('userpost/delete/<int:pk>', views.PostDeleteView.as_view()),
    path('comment/', views.CommentListView.as_view(), name='comment_list'),
    path('post/comment/', views.CommentListView.as_view(), name='comment_list'),
    path('userpost/comment/', views.CommentListView.as_view(), name='comment_list'),
    path('post/comment/new/', views.CommentCreateView.as_view(), name='comment_form'),
    path('userpost/comment/new/', views.CommentCreateView.as_view(), name='comment_form'),
    path('comment/new', views.CommentCreateView.as_view(), name='comment_new'),
    path('mailtoadmin/create/', views.mailtoadmin_create, name='mailtoadmin_create'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_done/', views.signup_done, name='signup_done'),
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    path('user/edit', views.UserUpdateView.as_view(), name='user_form'),
    path('', include('django.contrib.auth.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
