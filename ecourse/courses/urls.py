from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('courses/', views.index, name="index"),
    path('courses/<int:course_id>', views.list, name="list"),
    path('category/', views.CategoryView.as_view())
]