from sys import prefix
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView,UpdateView,DeleteView,CreateView,TemplateView
from django.views.generic.detail import BaseDetailView
from . import models
from .import forms
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from urllib.parse import urlparse
from django.shortcuts import resolve_url,redirect
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

User = get_user_model()

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name='dashboard.html'

    def get_context_data(self,**kwargs):
       context = super().get_context_data(**kwargs)
       context['page_title']="Dashboard"
       context['obj'] = models.Settings.objects.all()[0]
       return context

#SYSTEM SETTINGS
class ViewSystemSettings(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = models.Settings
    template_name = 'view_system_settings.html'
    permission_required = 'system.view_systemsettings'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view system settings'
    
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
        context["card_title"] = "Settings List"
        context['add_url'] = 'system:add-system-setting'
        context['del_url'] = reverse('system:delete-system-settings')
        context['page_title'] = 'settings'
        return context

class AddSystemSetting(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.Settings
    form_class = forms.SystemSettingsForm
    template_name = 'add_system_settings.html'  
    success_url = reverse_lazy("system:view-system-settings")
    permission_required = 'system.add_systemsettings'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add system settings'
    
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
        context["card_title"] = "Add Settings"
        context['save_url'] = 'system:add-system-setting'
        context['back_url'] = "system:view-system-settings"
        context['form_id'] = 'settings-form'
        context['page_title'] = 'settings'
        context['helper'] = forms.FormsetHelper()
        return context  

    def get(self, request,*args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        #form_class = self.get_form_class()
        Form = self.get_form_class()
        form = Form()
        context['form'] = form
        context['company_image_formset'] = forms.CompanyImageFormset(prefix="company_image")
        context['company_statement_formset'] = forms.CompanyStatementFormset(prefix="company_statement")
        context['company_admin_formset'] = forms.CompanyAdminFormset(prefix="company_admin")
        context['company_social_media_formset'] = forms.CompanySocialMediaFormset(prefix="company_social_media")
        return self.render_to_response(context)


    def post(self, request,*args,**kwargs):
        self.object = None
        #form_class = self.get_form_class()
        Form = self.form_class
        form = Form(self.request.POST,self.request.FILES)
        company_image_formset = forms.CompanyImageFormset(self.request.POST,self.request.FILES,prefix="company_image")
        company_statement_formset = forms.CompanyStatementFormset(self.request.POST,self.request.FILES,prefix="company_statement")
        company_admin_formset = forms.CompanyAdminFormset(self.request.POST,self.request.FILES,prefix="company_admin") 
        company_social_media_formset = forms.CompanySocialMediaFormset(self.request.POST,prefix="company_social_media")

        if (form.is_valid() and company_image_formset.is_valid() and 
            company_statement_formset.is_valid() and
            company_admin_formset.is_valid() and company_social_media_formset.is_valid()
            ):   
            return self.form_valid(form,company_image_formset,
                company_statement_formset,company_admin_formset,
                company_social_media_formset
                )
        else:
            return self.form_invalid(form,company_image_formset,
                company_statement_formset,company_admin_formset,
                company_social_media_formset
                )

    def form_valid(self,form,company_image_formset,
                company_statement_formset,company_admin_formset,
                company_social_media_formset
                ):
        self.object = form.save()

        company_image_formset.instance = self.object
        company_image_formset.save()

        company_statement_formset.instance = self.object
        company_statement_formset.save()

        company_admin_formset.instance = self.object
        company_admin_formset.save()

        company_social_media_formset.instance = self.object
        company_social_media_formset.save()

        return redirect(self.get_success_url())

    def form_invalid(self,form,company_image_formset,
            company_statement_formset,company_admin_formset,
            company_social_media_formset
            ):
        context = self.get_context_data()
        context['form'] = form
        context['company_image_formset'] = company_image_formset
        context['company_statement_formset'] = company_statement_formset
        context['company_admin_formset'] = company_admin_formset
        context['company_social_media_formset'] = company_social_media_formset
        return self.render_to_response(context)

class UpdateSystemSetting(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = models.Settings
    form_class = forms.SystemSettingsForm
    template_name='add_system_settings.html' 
    success_url = reverse_lazy("system:view-system-settings")
    permission_required = 'system.change_systemsettings'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to system settings'
    
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
        context['save_url'] = 'system:update-system-setting'
        context['back_url'] = "system:view-system-settings"
        context['form_id'] = 'settings-form'
        context['page_title'] = 'settings'
        context['helper'] = forms.FormsetHelper()
        return context  

    def get(self, request,*args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        #form_class = self.get_form_class()
        context['company_image_formset'] = forms.CompanyImageFormset(instance = self.object,prefix = "company_image")
        context['company_statement_formset'] = forms.CompanyStatementFormset(instance = self.object,prefix = "company_statement")
        context['company_admin_formset'] = forms.CompanyAdminFormset(instance = self.object,prefix = "company_admin") 
        context['company_social_media_formset'] = forms.CompanySocialMediaFormset(instance = self.object,prefix = "company_social_media")
        return self.render_to_response(context)


    def post(self, request,*args,**kwargs):
        self.object = self.get_object()
        #form_class = self.get_form_class()
        Form = self.form_class
        form = Form(self.request.POST,self.request.FILES,instance = self.object)
        company_image_formset = forms.CompanyImageFormset(self.request.POST,self.request.FILES,instance = self.object,prefix="company_image")
        company_statement_formset = forms.CompanyStatementFormset(self.request.POST,self.request.FILES,instance = self.object,prefix="company_statement")
        company_admin_formset = forms.CompanyAdminFormset(self.request.POST,self.request.FILES,instance = self.object,prefix="company_admin") 
        company_social_media_formset = forms.CompanySocialMediaFormset(self.request.POST,instance = self.object, prefix="company_social_media")
        if (form.is_valid() and company_image_formset.is_valid() and 
            company_statement_formset.is_valid() and
            company_admin_formset.is_valid() and company_social_media_formset.is_valid()
            ):   
            return self.form_valid(form,company_image_formset,
                company_statement_formset,company_admin_formset,
                company_social_media_formset
                )
        else:
            return self.form_invalid(form,company_image_formset,
                company_statement_formset,company_admin_formset,
                company_social_media_formset
                )

    def form_valid(self,form,company_image_formset,
        company_statement_formset,company_admin_formset,
        company_social_media_formset
        ):
        
        self.object = form.save()

        company_image_formset.instance = self.object
        company_image_formset.save()

        company_statement_formset.instance = self.object
        company_statement_formset.save()

        company_admin_formset.instance = self.object
        company_admin_formset.save()

        company_social_media_formset.instance = self.object
        company_social_media_formset.save()

        return super().form_valid(form)
        #return redirect(self.get_success_url())

    def form_invalid(self,form,company_image_formset,
            company_statement_formset,company_admin_formset,
            company_social_media_formset
            ):
        context = self.get_context_data()
        context['form'] = form
        context['company_image_formset'] = company_image_formset
        context['company_statement_formset'] = company_statement_formset
        context['company_admin_formset'] = company_admin_formset
        context['company_social_media_formset'] = company_social_media_formset
        return self.render_to_response(context)
    
#@method_decorator(ensure_csrf_cookie, name='dispatch')
class DeleteSystemSetting(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = models.Settings
    permission_required = 'system.delete_systemsettings'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete system settings'

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
    
    def post(self, request,*args, **kwargs):
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

#CONTACT MESSAGES
class ViewContactMessages(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = models.ContactMessage
    template_name = 'view_contact_messages.html'
    paginate_by = 10
    ordering = ['date_sent']
    permission_required = 'system.view_contactmessages'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view user conatct messages'

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
        context["card_title"] = "User Contact Message List"
        context['add_url'] = None
        context['del_url'] = reverse('system:delete-contact-messages')
        context['page_title'] = 'Contact Messages'
        return context

class ViewContactMessageDetail(LoginRequiredMixin,PermissionRequiredMixin,BaseDetailView):
    model = models.ContactMessage
    permission_required = 'system.change_contactmessages'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view user contact message'

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context['name'] = self.object.full_name
            context['email'] = self.object.email_address
            context['message'] = self.object.text_message
            context['date'] = self.object.date_sent
       
            """ context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object """
        #context.update(kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        #msg_data = {"name":self.object.full_name, "email": self.object.email_address, "message":self.object.text_message}
        context = self.get_context_data()
        print(f'message object : {self.object.full_name}')
        return JsonResponse(context)

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

class DeleteContactMessage(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = models.ContactMessage
    permission_required = 'system.delete_contactmessage'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete user contact messages'

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
    
    def post(self, request,*args, **kwargs):
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
                    id_errors.append(f'bject with {id} does not exist')
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)


#NEWS LETTERS
class ViewNewsletterSubscriptions(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = models.NewsletterSubscription
    template_name = 'view_newsletter_subscriptions.html'
    paginate_by = 10
    ordering = ['subscription_date']
    permission_required = 'system.view_newslettersubcription'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view newsletter subcription'

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
        context["card_title"] = "Newsletter Subscription List"
        context['add_url'] = None
        context['del_url'] = reverse('system:delete-newsletter-subscriptions')
        context['page_title'] = 'Newsletter Subscription'
        return context

class DeleteNewsletterSubscription(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = models.NewsletterSubscription
    permission_required = 'system.delete_newslettersubscription'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete newslettersubscription'

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
    
    def post(self, request,*args, **kwargs):
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
                    id_errors.append(f'bject with {id} does not exist')
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)


