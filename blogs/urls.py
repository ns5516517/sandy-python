from django.urls import path
from blogs import views

urlpatterns = [
    path("blogs/", views.getAllBlogs, name="blogs"),
    path("blog_detail/", views.getOneBlog, name="blog_detail"),
]
