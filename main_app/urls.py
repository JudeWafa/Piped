from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
   path('',views.mainpage, name='mainpage'),
   path('pipelines/create/', views.create_pipeline, name='create_pipeline'),
   path('pipelines/<int:pipeline_id>/', views.pipeline_detail, name='pipeline_detail'),
   path('move_item/', views.move_item, name='move_item'),
   path('pipelines/view_pipelines/', views.viewAllPipelines, name='view_all'),
]
