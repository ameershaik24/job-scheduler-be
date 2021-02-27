from django.urls import path

from . import views

urlpatterns = [
    path('get_jobs_requested/', views.get_jobs_requested),
    path('create_job/', views.create_job),
    path('delete_job/<str:pk>/', views.delete_job),
    path('pause_play_job/<str:pk>/<str:is_paused>/', views.pause_play_job)
]