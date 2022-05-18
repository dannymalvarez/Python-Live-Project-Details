from django.urls import path
from . import views

urlpatterns = [
    path('', views.Best_Cities_home, name='Best_Cities_home'), #if there is no path in the url it send them to my site's home page
    path('create/', views.Best_Cities_create, name='Best_Cities_create'), #this calls the function to create the create page
    path('topcities/', views.Best_Cities_topcities, name='Best_Cities_topcities'), #This calls the function to view the top cities
    path('details/<int:pk>/', views.Best_Cities_details, name='Best_Cities_details'), #This calls the function to view the details from those top cities
    path('delete/<int:pk>/', views.Best_Cities_delete, name='Best_Cities_delete'),
    path('edit/<int:pk>/', views.Best_Cities_edit, name='Best_Cities_edit'),
    path('weather/', views.Best_Cities_weather, name='Best_Cities_weather'),
    path('scrape/', views.Best_Cities_scrape, name='Best_Cities_scrape'),
    ]