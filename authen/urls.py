from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('picture/', views.picture, name="picture"),
	path('upload_picture/', views.upload_picture, name='upload_picture'),
    path('save_uploaded_picture/', views.save_uploaded_picture, name='save_uploaded_picture'),
	path('password/', views.password, name="password"),
	path('settings/', views.settings, name="settings"),
	path('register/', views.register, name="register"),
	path('login/', auth_views.login, {'template_name': 'authen/login.html'}, name='login'),
	path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
	path('<str:username>/', views.profile, name="profile"),
	path('activate/<str:token>/', views.activate, name="activate"),
	path('test2_view', views.test2_view) # 测试国际化
]