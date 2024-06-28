from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('indexes', views.indexes, name='indexes'),
    path('new_page', views.new_page, name='new_page'),
    path('edit_page/<int:page_id>/', views.edit_page, name='edit_page'),
    path('view_page/<int:page_id>/', views.view_page, name='view_page'),
    path('random_page', views.random_page, name='random_page'),
    path('login/', auth_views.LoginView.as_view(template_name='wikinow/login.html'), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
]
