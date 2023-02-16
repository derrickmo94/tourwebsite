from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from . import models
from django.contrib.auth.models import Group
from .import forms
from django.contrib.auth import REDIRECT_FIELD_NAME, views as auth_views
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from urllib.parse import urlparse
from django.shortcuts import resolve_url,redirect
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

User = get_user_model()

#ADMIN AUTHENTICATION
class AdminLogin(auth_views.LoginView):
    form_class = forms.AdminLoginForm
    template_name = "login.html"

#USER GROUP
class ViewUserGroups(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = Group
    template_name = 'view_user_groups.html'
    ordering = ['name']
    paginate_by = 10
    permission_required = 'auth.view_group'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view user groups'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Group List"
        context['add_url'] = 'user:add-user-group'
        context['del_url'] = reverse('user:delete-user-groups')
        context['page_title'] = 'user groups'
        return context

class AddUserGroup(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Group
    form_class = forms.UserGroupForm
    template_name = 'add_user_group.html'  
    success_url = reverse_lazy("user:view-user-groups")
    permission_required = 'auth.add_group'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add user groups'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Add Group"
        context['save_url'] = 'user:add-user-group'
        context['back_url'] = "user:view-user-groups"
        context['form_id'] = 'user-group-form'
        context['page_title'] = 'User group'
        return context

class UpdateUserGroup(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Group
    form_class = forms.UserGroupForm
    template_name = 'add_user_group.html' 
    success_url = reverse_lazy("user:view-user-groups")
    permission_required = 'auth.change_group'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to change user groups'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Update Group"
        context['save_url'] = 'user:update-user-group'
        context['back_url'] = "user:view-user-groups"
        context['form_id'] = 'user-group-form'
        context['page_title'] = 'User group'
        return context

class DeleteUserGroup(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Group
    permission_required = 'auth.delete_group'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete user groups'

    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)

    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            context = {}
            context['path'] = path
            context['resolved+login_url'] = resolved_login_url
            context['redirect_field']= self.get_redirect_field_name()
            return JsonResponse(context) 
    
    def post(self, request): 
        context ={}
        deleted_ids = []
        id_errors =[] 
        ids = request.POST.getlist('data[]')
        id = request.POST.get('data')

        print(f'POST IDs: {ids} and ID: {id}')
     
        if id is not None:
            self.model.objects.get(pk = id).delete()
            deleted_ids.append(id)  
            print(f'DELETED ids {deleted_ids}')

        if ids is not None:
            for id in ids:         
                if id is not None:
                    self.model.objects.get(pk = id).delete()
                    deleted_ids.append(id)                           
                else:
                    id_errors.append(f"Object with {id} does not exist")
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)


#USERS
class ViewChangeAdminUserPassword(LoginRequiredMixin,PermissionRequiredMixin,auth_views.PasswordChangeView):
    form_class = forms.UserAdminPasswordChangeForm
    success_url = reverse_lazy('user:view-users')
    template_name = 'change_admin_user_password.html'
    permission_required = 'user.change_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to users'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "User Password"
        context['page_title']="Change Password"
        context['back_url'] = "user:view-users"
        context['form_id'] = 'change-user-password-form'
        return context

class ViewUsers(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = User
    queryset = User.objects.all().exclude(customer_user_profile__is_customer = True)
    template_name = 'view_user_profiles.html'
    paginate_by = 10
    ordering = ['username']
    permission_required = 'user.view_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view users'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "User List"
        context['add_url'] = 'user:add-user'
        context['del_url'] = reverse('user:delete-users')
        context['page_title'] = 'User Profile'
        return context

class AddUser(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model =  User
    form_class = forms.UserForm
    template_name = 'add_user_profile.html'  
    success_url = reverse_lazy("user:view-users")
    permission_required = 'user.add_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add users'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Add User"
        context['save_url'] = 'user:add-user'
        context['back_url'] = "user:view-users"
        context['form_id'] = 'admin-user-form'
        context['page_title'] = 'User Profile'    
        return context

    def get(self, request,*args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        #form_class = self.get_form_class()
        Form = self.get_form_class()
        form = Form()
        context['form'] = form
        context['admin_form'] = forms.AdminUserForm()
        return self.render_to_response(context)


    def post(self, request,*args,**kwargs):
        self.object = None
        #form_class = self.get_form_class()
        Form = self.form_class
        form = Form(self.request.POST,self.request.FILES)
        admin_form = forms.AdminUserForm(self.request.POST,self.request.FILES)  

        if  form.is_valid() and admin_form.is_valid():   
            return self.form_valid(form,admin_form)
        else:
            return self.form_invalid(form,admin_form)

    def form_valid(self,form,admin_form):
        self.object = form.save()
        if admin_form.instance is None:
            admin_form.instance.user = self.object
            admin_form.save()
        else:
            admin_form = forms.AdminUserForm(self.request.POST,self.request.FILES,instance = self.object.admin_user_profile)  
            admin_form.save()
        return redirect(self.get_success_url())

    def form_invalid(self,form,admin_form):
        context = self.get_context_data()
        context['form'] = form
        context['admin_form'] = admin_form
        return self.render_to_response(context)
   
class UpdateUser(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model =  User
    form_class = forms.UserChangeForm
    template_name = 'add_user_profile.html' 
    success_url = reverse_lazy("user:view-users")
    permission_required = 'user.change_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to users'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Update User"
        context['save_url'] = 'user:update-user'
        context['back_url'] = "user:view-users"
        context['form_id'] = 'admin-user-form'
        context['page_title'] = 'User Profile'    
        return context

    def get(self, request,*args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        #form_class = self.get_form_class()
        Form = self.form_class
        context['form'] = Form(instance = self.object)
        context['admin_form'] = forms.AdminUserForm(instance = self.object.admin_user_profile)
        return self.render_to_response(context)


    def post(self, request,*args,**kwargs):
        self.object = self.get_object()
        #form_class = self.get_form_class()
        Form = self.form_class
        form = Form(self.request.POST,self.request.FILES,instance = self.object)
        admin_form = forms.AdminUserForm(self.request.POST,self.request.FILES, instance = self.object.admin_user_profile)  

        if form.is_valid() and admin_form.is_valid():   
            return self.form_valid(form,admin_form)
        else:
            return self.form_invalid(form,admin_form)

    def form_valid(self,form,admin_form):
        self.object = form.save()
        admin_form.instance.user = self.object
        admin_form.save()
        return redirect(self.get_success_url())

    def form_invalid(self,form,admin_form):
        context = self.get_context_data()
        context['form'] = form
        context['admin_form'] = admin_form
        return self.render_to_response(context)

class DeleteUser(LoginRequiredMixin,PermissionRequiredMixin,DeleteView): 
    model = User
    permission_required = 'user.delete_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete users'

    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)

    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            context = {}
            context['path'] = path
            context['resolved+login_url'] = resolved_login_url
            context['redirect_field']= self.get_redirect_field_name()
            return JsonResponse(context) 

    def post(self, request):
        context ={}
        deleted_ids = []
        id_errors =[] 
        ids = request.POST.getlist('data[]')
        id = request.POST.get('data')

        print(f'POST IDs: {ids} and ID: {id}')
     
        if id is not None:
            self.model.objects.get(pk=id).delete()
            deleted_ids.append(id)  
            print(f'DELETED ids {deleted_ids}')

        if ids is not None:
            for id in ids:         
                if id is not None:
                    self.model.objects.get(pk=id).delete()
                    deleted_ids.append(id)                           
                else:
                    id_errors.append(f"Object with {id} does not exist")
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)


#CUSTOMER TYPE
class ViewCustomerTypes(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = models.CustomerType
    template_name = 'view_customer_type.html'
    paginate_by = 10
    ordering = ['type_name']
    permission_required = 'user.view_customertype'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view customer types'

    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "customer Type List"
        context['add_url'] = 'user:add-customer-type'
        context['del_url'] = reverse('user:delete-customer-types')
        context['page_title'] = 'Customer type'
        return context

class AddCustomerType(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.CustomerType
    form_class = forms.CustomerTypeForm
    template_name = 'add_customer_type.html'  
    success_url = reverse_lazy("user:view-customer-types")
    permission_required = 'user.add_customertype'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add customer type'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Add Customer Type"
        context['save_url'] = 'user:add-customer-type'
        context['back_url'] = "user:view-customer-types"
        context['form_id'] = 'customer-type-form'
        context['page_title'] = 'customer type'
        return context

class UpdateCustomerType(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = models.CustomerType
    form_class = forms.CustomerTypeForm
    template_name = 'add_customer_type.html' 
    success_url = reverse_lazy("user:view-customer-types")
    permission_required = 'user.change_customertype'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to customer type'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Update Customer Type"
        context['save_url'] = 'user:update-customer-type'
        context['back_url'] = "user:view-customer-types"
        context['form_id'] = 'customer-type-form'
        context['page_title'] = 'customer type'
        return context

class DeleteCustomerType(LoginRequiredMixin,DeleteView):
    model = models.CustomerType
    permission_required = 'user.delete_customertype'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete customer type'

    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)

    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            context = {}
            context['path'] = path
            context['resolved+login_url'] = resolved_login_url
            context['redirect_field']= self.get_redirect_field_name()
            return JsonResponse(context) 
    
    def post(self, request): 
        context ={}
        deleted_ids = []
        id_errors =[] 
        ids = request.POST.getlist('data[]')
        id = request.POST.get('data')

        print(f'POST IDs: {ids} and ID: {id}')
     
        if id is not None:
            self.model.objects.get(pk = id).delete()
            deleted_ids.append(id)  
            print(f'DELETED ids {deleted_ids}')

        if ids is not None:
            for id in ids:         
                if id is not None:
                    self.model.objects.get(pk = id).delete()
                    deleted_ids.append(id)                           
                else:
                    id_errors.append(f"Object with {id} does not exist")
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)

#CUSTOMER
class ViewChangeCustomerUserPassword(LoginRequiredMixin,PermissionRequiredMixin,auth_views.PasswordChangeView):
    form_class = forms.UserAdminPasswordChangeForm
    success_url = reverse_lazy('user:view-customers')
    template_name = 'change_admin_user_password.html'
    permission_required = 'user.change_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to customer users password'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Customer User Password"
        context['page_title']="Change Password"
        context['back_url'] = "user:view-customers"
        context['form_id'] = 'change-user-password-form'
        return context

class ViewCustomers(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = User
    queryset = User.objects.all().filter(customer_user_profile__is_customer=True)
    template_name = 'view_customers.html'
    paginate_by = 10
    permission_required = 'user.view_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view customers'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Customer List"
        context['add_url'] = 'user:add-customer'
        context['del_url'] = reverse('user:delete-customers')
        context['page_title'] = 'customers'
        return context

class AddCustomer(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = User
    form_class = forms.CustomerUserVersionUserForm
    template_name = 'add_customer.html'  
    success_url = reverse_lazy("user:view-customers")
    permission_required = 'user.add_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add customers'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Add Customer"
        context['save_url'] = 'user:add-customer'
        context['back_url'] = "user:view-customers"
        context['form_id'] = 'customer-user-form'
        context['page_title'] = 'customers'
        return context

    def get(self, request,*args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        #form_class = self.get_form_class()
        #Form = self.get_form_class()
        #form = Form()
        #context['form'] = form
        context['customer_form'] = forms.CustomerUserForm()
        return self.render_to_response(context)


    def post(self, request,*args,**kwargs):
        self.object = None
        #form_class = self.get_form_class()
        Form = self.form_class
        form = Form(self.request.POST,self.request.FILES)
        customer_form = forms.CustomerUserForm(self.request.POST,self.request.FILES)  

        if  form.is_valid() and customer_form.is_valid():   
            return self.form_valid(form,customer_form)
        else:
            return self.form_invalid(form,customer_form)

    def form_valid(self,form,customer_form):
        self.object = form.save()
        if customer_form.instance is None:
            customer_form.instance.user = self.object
            customer_form.save()
        else:
            customer_form = forms.CustomerUserForm(self.request.POST,self.request.FILES,instance = self.object.customer_user_profile) 
            customer_form.save()
        return redirect(self.get_success_url())

    def form_invalid(self,form,customer_form):
        context = self.get_context_data()
        context['form'] = form
        context['customer_form'] = customer_form
        return self.render_to_response(context)

class UpdateCustomer(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = User
    form_class = forms.CustomerUserChangeForm  
    template_name = 'add_customer.html' 
    success_url = reverse_lazy("user:view-customers")
    permission_required = 'user.change_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to customer'
    
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)
    
    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())

        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Update Customer"
        context['save_url'] = 'user:update-customer'
        context['back_url'] = "user:view-customers"
        context['form_id'] = 'customer-user-form'
        context['page_title'] = 'customers'
        return context

    def get(self, request,*args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        #form_class = self.get_form_class()
        Form = self.form_class
        context['form'] = Form(instance = self.object)
        context['customer_form'] = forms.CustomerUserForm(instance = self.object.customer_user_profile)
        return self.render_to_response(context)


    def post(self, request,*args,**kwargs):
        self.object = self.get_object()
        #form_class = self.get_form_class()
        Form = self.form_class
        form = Form(self.request.POST,self.request.FILES,instance = self.object)
        customer_form = forms.CustomerUserForm(self.request.POST,self.request.FILES,instance = self.object.customer_user_profile)  

        if form.is_valid() and customer_form.is_valid():   
            return self.form_valid(form,customer_form)
        else:
            return self.form_invalid(form,customer_form)

    def form_valid(self,form,customer_form):
        self.object = form.save()

        customer_form.instance.user = self.object
        customer_form.save()
        return redirect(self.get_success_url())

    def form_invalid(self,form,customer_form):
        context = self.get_context_data()
        context['form'] = form
        context['customer_form'] = customer_form
        return self.render_to_response(context)

class DeleteCustomer(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = User
    permission_required = 'user.delete_user'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete customers'

    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)

    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
            messages.error(self.request,self.permission_denied_message)
            context = {}
            context['path'] = path
            context['resolved+login_url'] = resolved_login_url
            context['redirect_field']= self.get_redirect_field_name()
            return JsonResponse(context) 
    
    def post(self, request): 
        context ={}
        deleted_ids = []
        id_errors =[] 
        ids = request.POST.getlist('data[]')
        id = request.POST.get('data')

        print(f'POST USER IDs {ids} and USER ID {id}')
     
        if id is not None:
            self.model.objects.get(id=id).delete()
            deleted_ids.append(id)  
            print(f'DELETED ids {deleted_ids}')

        if ids is not None:
            for id in ids:         
                if id is not None:
                    self.model.objects.get(id=id).delete()
                    deleted_ids.append(id)                           
                else:
                    id_errors.append(f"User with {id} does not exist")
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)
