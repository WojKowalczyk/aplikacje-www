from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

from . import views

app_name = "polls"
urlpatterns = [
    path('persons/', views.person_list),
    path('persons/<int:pk>/', views.person_detail),
    path('persons/update/<int:pk>/', views.person_update),
    path('persons/delete/<int:pk>/', views.person_delete),
    path('stanowisko/<int:id>/members',views.stanowisko_members, name='stanowisko_members'),
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
] + debug_toolbar_urls()