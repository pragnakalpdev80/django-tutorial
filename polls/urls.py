from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

# app_name = "polls"
# urlpatterns = [
#     path("", views.index, name="index"),
#     path("<int:question_id>/", views.detail, name="detail"),
#     path("<int:question_id>/results/", views.results, name="results"),
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]

app_name = "polls"
urlpatterns = [
    path("login/", views.login,name="login"),
    path("index/", views.index,name="index2"),
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),                                                                                                                                       
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.VoteView.as_view(), name="vote"),
    path("register/", views.register, name="register"),
]

