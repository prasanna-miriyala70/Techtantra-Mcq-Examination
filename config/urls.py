from django.contrib import admin
from django.urls import path
from exam import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.instructions, name="instructions"),
    path("register/", views.register_candidate, name="register"),
    path("exam/", views.exam, name="exam"),
    path("submit/", views.submit_exam, name="submit_exam"),
    path("result/<int:attempt_id>/", views.result, name="result"),
]
