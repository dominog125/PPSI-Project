from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from . import views
from .views import ThreadListAPIView, ThreadDetailAPIView

urlpatterns = [
    path('', views.category_list, name='category_list'),  # Home page showing top categories
    path('forums/', views.all_categories, name='all_categories'),  # All forums
    path('forum/<int:category_id>/', views.thread_list, name='thread_list'),  # Threads in a specific forum
    path('thread/<int:thread_id>/', views.post_list, name='post_list'),  # Posts in a specific thread
    path('thread/create/', views.create_thread, name='create_thread'),  # Create a new thread
    path('post/create/<int:thread_id>/', views.create_post, name='create_post'),  # Create a new post
    path('register/', views.register, name='register'),  # User registration
    path('login/', views.user_login, name='login'),  # User login
    path('logout/', views.logout_view, name='logout'),  # User logout
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),  # Edit a post
    path('set_language/', views.set_language, name='set_language'),  # Language change URL
    path('threads/', ThreadListAPIView.as_view(), name='thread-list'),
    path('threads/<int:pk>/', ThreadDetailAPIView.as_view(), name='thread-detail'),
]
