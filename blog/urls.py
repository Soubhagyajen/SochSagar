from django.contrib import admin
from django.urls import path,include
from . import views
from .views import home,blog_list,create_blog,blog_detail,blog_update,delete_blog
from django.conf import settings
from django.conf.urls.static import static
from .views import register,about,display_image
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('',views.home,name="home" ),
    path('',views.blog_list,name="blog_list"),
    path('create/',views.create_blog,name="create"),
    path('update/<int:id>/', views.blog_update, name="blog_update"),
    path('delete/<int:id>/', views.delete_blog, name="delete_blog"),
    # path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path("register/", register, name="register"),
    # path('<int:id>/', blog_detail, name="blog_detail"),
    path('<int:id>/', views.blog_detail, name="blog_detail"),
    path("login/", auth_views.LoginView.as_view(template_name="register/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("about/", views.about, name="about"),
    path('image/<int:post_id>/', display_image, name='display_image'),
     path('like/<int:post_id>/', views.like_post, name='like_post'),
      path('search/', views.search_posts, name='search_posts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)