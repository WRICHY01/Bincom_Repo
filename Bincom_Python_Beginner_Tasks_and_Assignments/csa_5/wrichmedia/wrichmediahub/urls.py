from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name = "home"),
    path("post/create/", views.create_post_view, name="create_post"),
    path("post/<int:pk>/", views.post_detail_view, name="post_detail"),
    path("post/<int:pk>/delete/", views.delete_post_view, name="delete_post")
]