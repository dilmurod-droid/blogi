from django.conf import settings
from django.urls import path, include

from blog.views import Home, About, BlogDetailView, contact_view, Delete, Update, Create, mark_notification_as_read, \
    NotificationListView, like_post, comment_post, comment_delete, UserProfileDetailView

urlpatterns = [
    path('', Home.as_view(),name="home"),
    path('about/', About.as_view(), name="about"),
    path('create/', Create.as_view(), name="create"),
    path('notifications/mark_as_read/<int:pk>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('detail/<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('contact/', contact_view, name='contact'),
    path('delete/<slug:slug>/', Delete.as_view(), name='delete'),
    path('update/<slug:slug>/', Update.as_view(), name='update'),
    # path('blog/<slug:slug>/like/', BlogLikeView.as_view(), name='like_post'),
    path('blog/<slug:slug>/like/',like_post, name='like_post'),
    path('blog/<slug:slug>/comment/', comment_post, name='comment_post'),
    path('blog/<slug:slug>/comment/delete/', comment_delete, name='comment_delete'),
    path('other/profile/<str:username>/', UserProfileDetailView.as_view(), name='view_profile')
]
