from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('', views.view, name='view'),
    path('summary/<int:material_id>/', views.summary_study_material, name='summary_study_material'),
    path('quiz/<int:material_id>/', views.quiz_study_material, name='quiz_study_material'),
    path('edit/<int:material_id>/', views.edit, name='edit'),
    path('delete/<int:material_id>/', views.delete, name='delete'),
]