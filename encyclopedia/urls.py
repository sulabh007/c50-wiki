from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>", views.editpage, name="editpage"),
    path("save/", views.savepage, name="save"),
    path("random/", views.random, name="random"),
    path("wiki/<str:title>", views.topic, name="topic"),
    path("?q=<str:query>", views.search, name="search")
]
