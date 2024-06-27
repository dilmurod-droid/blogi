from django.urls import path

from .views import logout_view, login_view, RegisterView, Profile, EditProfileView, users_accs

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('profile/<str:username>/', Profile.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/update/',  EditProfileView.as_view(), name='edit_profile'),
    path('user/<str:username>/',users_accs.as_view(),name='userprofile')

]