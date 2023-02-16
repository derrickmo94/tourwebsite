from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views

app_name = "user"
urlpatterns = [
    path('account/login/',user_views.AdminLogin.as_view(),name="login"),
    #path('login/',auth_views.LoginView.as_view(template_name='login.html'),name="login"),
    path('logout/',auth_views.LogoutView.as_view(),name="logout"),
    #path('system/user/<int:pk>/password/',tour_views.ViewChangeAdminUserPassword,name="change-password"),

    path('account/user/password/',user_views.ViewChangeAdminUserPassword.as_view(),name='change-user-password'),
    path('account/users',user_views.ViewUsers.as_view(),name='view-users'),
    path('account/user/add',user_views.AddUser.as_view(),name='add-user'),
    path('account/user/<int:pk>/',user_views.UpdateUser.as_view(),name='update-user'),
    path('account/user/<int:pk>/delete',user_views.DeleteUser.as_view(),name='delete-user'),
    path('account/user/delete',user_views.DeleteUser.as_view(),name='delete-users'),

    path('account/user-groups',user_views.ViewUserGroups.as_view(),name='view-user-groups'),
    path('account/user-group/add',user_views.AddUserGroup.as_view(),name='add-user-group'),
    path('account/user-group/<int:pk>/',user_views.UpdateUserGroup.as_view(),name='update-user-group'),
    path('account/user-group/<int:pk>/delete',user_views.DeleteUserGroup.as_view(),name='delete-user-group'),
    path('account/user-group/delete',user_views.DeleteUserGroup.as_view(),name='delete-user-groups'),

    path('customers/types',user_views.ViewCustomerTypes.as_view(),name='view-customer-types'),
    path('customers/type/add',user_views.AddCustomerType.as_view(),name='add-customer-type'),
    path('customers/type/<int:pk>/',user_views.UpdateCustomerType.as_view(),name='update-customer-type'),
    path('customers/type/<int:pk>/delete',user_views.DeleteCustomerType.as_view(),name='delete-customer-type'),
    path('customers/type/delete',user_views.DeleteCustomerType.as_view(),name='delete-customer-types'),

    path('customer/password/',user_views.ViewChangeCustomerUserPassword.as_view(),name='change-customer-password'),
    path('customers',user_views.ViewCustomers.as_view(),name='view-customers'),
    path('customer/add',user_views.AddCustomer.as_view(),name='add-customer'),
    path('customer/<int:pk>/',user_views.UpdateCustomer.as_view(),name='update-customer'),
    path('customer/<int:pk>/delete',user_views.DeleteCustomer.as_view(),name='delete-customer'),
    path('customer/delete',user_views.DeleteCustomer.as_view(),name='delete-customers'),
]