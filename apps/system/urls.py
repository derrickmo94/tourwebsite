from django.urls import path
from . import views as system_views

app_name = "system"
urlpatterns = [
    path('',system_views.Dashboard.as_view(),name='dashboard'),
    path('system/settings',system_views.ViewSystemSettings.as_view(),name='view-system-settings'),
    path('system/setting/add',system_views.AddSystemSetting.as_view(),name='add-system-setting'),
    path('system/setting/<int:pk>/',system_views.UpdateSystemSetting.as_view(),name='update-system-setting'),
    path('system/setting/<int:pk>/delete',system_views.DeleteSystemSetting.as_view(),name='delete-system-setting'),
    path('system/setting/delete',system_views.DeleteSystemSetting.as_view(),name='delete-system-settings'),

    path('messages/contact',system_views.ViewContactMessages.as_view(),name='view-contact-messages'),
    path('messages/contact/<int:pk>/',system_views.ViewContactMessageDetail.as_view(),name='contact-message-detail'),
    path('messages/contact/<int:pk>/delete',system_views.DeleteContactMessage.as_view(),name='delete-contact-message'),
    path('messages/contact/delete',system_views.DeleteContactMessage.as_view(),name='delete-contact-messages'),

    path('news/subscriptions',system_views.ViewNewsletterSubscriptions.as_view(),name='view-newsletter-subscriptions'),
    path('news/subscriptions/<int:pk>/delete',system_views.DeleteNewsletterSubscription.as_view(),name='delete-newsletter-subscription'),
    path('news/subscriptions/delete',system_views.DeleteNewsletterSubscription.as_view(),name='delete-newsletter-subscriptions'),
]