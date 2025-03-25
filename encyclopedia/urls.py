from django.urls import path

from . import views
app_name="encyclopedia"
urlpatterns = [
    path("<str:name>",views.call,name="call"),
    path("search/",views.search, name="search"),
    path("", views.index, name="index"),
    path("random/",views.random_entry,name="random"),
    path("create_content",views.create_content, name="create_content"),
    path("edit",views.go_edit, name="go_edit"),
    path("edit/<str:name>",views.edit_page, name="edit"),
    path("save",views.save_edit,name="save"),
    
]
