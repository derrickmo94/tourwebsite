from sys import prefix
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView,DetailView,UpdateView,DeleteView,CreateView
from django.views.generic.detail import BaseDetailView
from . import models
from .import forms
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from urllib.parse import urlparse
from django.shortcuts import resolve_url
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model

User = get_user_model()

#TOUR DESTINATION
class ViewTourDestinations(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = models.TourDestination
    template_name = 'view_tour_destinations.html'
    paginate_by = 10
    ordering = ['name']
    permission_required = 'tour.view_tourdestination'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view destinations'
    

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
        context["card_title"] = "Destination List"
        context['add_url'] = 'tour:add-destination'
        context['del_url'] = reverse('tour:delete-destinations')
        context['page_title'] =  'Tour destinations'
        return context

class AddTourDestination(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.TourDestination
    form_class = forms.TourDestinationForm
    template_name = 'add_tour_destination.html'
    success_url = reverse_lazy("tour:view-destinations")
    permission_required = 'tour.add_tourdestination'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add destinations'

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
        context["card_title"] = "Add Destination"
        context['save_url'] = 'tour:add-destination'
        context['back_url'] = 'tour:view-destinations'
        context['form_id'] = 'tour-destination-form'
        context['page_title'] = 'Tour Destinations'
        return context

class UpdateTourDestination(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model = models.TourDestination
    form_class = forms.TourDestinationForm
    template_name = 'add_tour_destination.html' 
    success_url = reverse_lazy("tour:view-destinations")
    success_message ="%(name)s destination has been updated successfully!"
    permission_required = 'tour.change_tourdestination'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to destinations'
   
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
        context["card_title"] = "Update Destination"
        context['save_url'] = 'tour:update-destination'
        context['back_url'] = 'tour:view-destinations'
        context['form_id'] = 'tour-destination-form'
        context['page_title'] = 'Tour destinations'
        return context

class DeleteTourDestination(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model = models.TourDestination
    success_message = "%(name)s was successfully <strong>deleted!</strong>"
    permission_required = 'tour.change_tourdestination'
    permission_denied_message ="<strong>Access denied</strong> You don\'t have permission to delete destinations"
    
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
            self.model.objects.get(pk=id).delete()
            deleted_ids.append(id)  
            print(f'DELETED ids {deleted_ids}')

        if ids is not None:
            for id in ids:         
                if id is not None:
                    self.model.objects.get(pk=id).delete()
                    deleted_ids.append(id)                           
                else:
                    id_errors.append(f"User with {id} does not exist")
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)


#TOUR CATEGORY
class ViewTourCategories(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = models.TourCategory
    template_name = 'view_tour_categories.html'  
    ordering =  ['name']
    paginate_by = 10
    permission_required = 'tour.view_tourcategory'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view tour categories'
    
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
        context["card_title"] = "Category List"
        context['add_url']  = 'tour:add-tour-category'
        context['del_url'] = reverse('tour:delete-tour-categorys')
        context['page_title'] = 'Tour Category'
        return context

class AddTourCategory(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.TourCategory
    form_class = forms.TourCategoryForm
    template_name = 'add_tour_category.html'
    success_url = reverse_lazy("tour:view-tour-categories")
    permission_required = 'tour.add_tourcategory'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add tour category'
    

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
        context["card_title"] = "Add Category"
        context['save_url'] = 'tour:add-tour-category'
        context['back_url'] = "tour:view-tour-categories"
        context['form_id'] = 'tour-category-form'
        context['page_title'] = 'Tour Category'
        return context

class UpdateTourCategory(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = models.TourCategory
    form_class = forms.TourCategoryForm
    template_name = 'add_tour_category.html'
    success_url = reverse_lazy("tour:view-tour-categories")
    permission_required = 'tour.change_tourcategory'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to tour category'
    

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
        context["card_title"] = "Update Category"
        context['save_url'] = 'tour:update-tour-category'
        context['back_url'] = "tour:view-tour-categories"
        context['form_id'] = 'tour-category-form'
        context['page_title'] = 'Tour Category'
        return context

class DeleteTourCategory(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = models.TourCategory
    permission_required = 'tour.delete_tourcategory'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete tour category'

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
            self.model.objects.get(pk = id).delete()
            deleted_ids.append(id)  
            print(f'DELETED ids {deleted_ids}')

        if ids is not None:
            for id in ids:         
                if id is not None:
                    self.model.objects.get(pk = id).delete()
                    deleted_ids.append(id)                           
                else:
                    id_errors.append(f"User with {id} does not exist")
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)


#TOUR
class ViewTours(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = models.Tour
    template_name = 'view_tours.html'
    #ordering = ['name']
    paginate_by = 10
    permission_required = 'tour.view_tour'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view tours'
    
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
        context["card_title"] = "Tour List"
        context['add_url'] = 'tour:add-tour'
        context['del_url'] = reverse('tour:delete-tours')
        context['page_title'] = 'Tours'
        return context

class AddTour(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model = models.Tour
    form_class = forms.TourForm
    template_name = 'add_tour.html'
    success_url = reverse_lazy("tour:view-tours")
    success_message = "New %(name)s tour has been added successfully"
    permission_required = 'tour.add_tour'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add tour'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Add Tour"
        context['save_url'] = 'tour:add-tour'
        context['back_url'] = "tour:view-tours"
        context['form_id'] = 'tour-form'
        context['page_title'] = 'Tours'
        context['helper'] = forms.FormsetHelper()
        return context

    def get(self, request,*args, **kwargs):
        self.object = None
        context = self.get_context_data(**kwargs)
        #form_class = self.get_form_class()
        Form = self.get_form_class()
        form = Form()
        context['form'] = form
        context['tour_image_form'] = forms.TourImageFormset(prefix="tour_image")
        context['tour_related_form'] = forms.RelatedTourFormset(prefix="tour_related")
        context['tour_inclusion_form'] = forms.TourInclusionFormset(prefix="tour_inclusion")
        context['tour_insight_form'] = forms.TourInsightsFormset(prefix="tour_insight")
        context['tour_tag_form'] = forms.TourTagFormset(prefix="tour_tag")
        context['tour_program_form'] = forms.TourProgramFormset(prefix="tour_program")
        context['tour_question_form'] = forms.TourQuestionsFormset(prefix="tour_question")    

        return self.render_to_response(context)


    def post(self, request,*args,**kwargs):
        self.object = None
        #form_class = self.get_form_class()
        Form = self.get_form_class()
        tour_form = Form(self.request.POST,self.request.FILES)
        tour_image_form = forms.TourImageFormset(self.request.POST,self.request.FILES,prefix="tour_image")    
        tour_related_form = forms.RelatedTourFormset(self.request.POST,prefix="tour_related")
        tour_inclusion_form = forms.TourInclusionFormset(self.request.POST,prefix="tour_inclusion")
        tour_insight_form = forms.TourInsightsFormset(self.request.POST,prefix="tour_insight")
        tour_tag_form = forms.TourTagFormset(self.request.POST,prefix="tour_tag")
        tour_program_form = forms.TourProgramFormset(self.request.POST,prefix="tour_program")
        tour_question_form = forms.TourQuestionsFormset(self.request.POST,prefix="tour_question")  

        if (tour_form.is_valid() and tour_image_form.is_valid() and tour_related_form.is_valid() and
            tour_inclusion_form.is_valid() and tour_insight_form.is_valid() and 
            tour_tag_form.is_valid() and tour_program_form.is_valid() and 
            tour_question_form.is_valid()):   
            return self.form_valid(tour_form,tour_image_form,tour_related_form,
                tour_inclusion_form,tour_insight_form,tour_tag_form,
                tour_program_form,tour_question_form
                )
        else:
            return self.form_invalid(tour_form,tour_image_form,tour_related_form,
                tour_inclusion_form,tour_insight_form,tour_tag_form,
                tour_program_form,tour_question_form
                )

    def form_valid(
        self,form,tour_image_form,tour_related_form,tour_inclusion_form,
        tour_insight_form,tour_tag_form,tour_program_form,tour_question_form):
        self.object = form.save()

        tour_image_form.instance = self.object
        tour_image_form.save()

        tour_related_form.instance = self.object
        tour_related_form.save()

        tour_inclusion_form.instance = self.object
        tour_inclusion_form.save()

        tour_insight_form.instance = self.object
        tour_insight_form.save()

        tour_tag_form.instance = self.object
        tour_tag_form.save()

        tour_program_form.instance = self.object
        tour_program_form.save()

        tour_question_form.instance = self.object
        tour_question_form.save()

        return super().form_valid(form) #redirect(self.get_success_url())

    def form_invalid(
        self,form,tour_image_form,tour_related_form,tour_inclusion_form,
        tour_insight_form,tour_tag_form,tour_program_form,tour_question_form):
        context = self.get_context_data()
        context['form'] = form
        context['tour_image_form'] = tour_image_form
        context['tour_related_form'] = tour_related_form
        context['tour_inclusion_form'] = tour_inclusion_form
        context['tour_insight_form'] = tour_insight_form
        context['tour_tag_form'] = tour_tag_form
        context['tour_program_form'] = tour_program_form
        context['tour_question_form'] = tour_question_form
        return self.render_to_response(context)
    
class UpdateTour(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model = models.Tour
    form_class = forms.TourForm
    template_name = 'add_tour.html'
    success_url = reverse_lazy("tour:view-tours")
    success_message ="%(name)s tour has been updated successfully!"
    permission_required = 'tour.change_tour'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add tour'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Update Tour"
        context['save_url'] = 'tour:update-tour'
        context['back_url'] = "tour:view-tours"
        context['form_id'] = 'tour-form'
        context['page_title'] = 'Tours'
        context['helper'] = forms.FormsetHelper()
        return context

    def get(self, request,*args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        #form_class = self.get_form_class()
        #Form = self.get_form_class()
        #form = Form(instance = self.object)
        #context['form'] = form
        context['tour_image_form'] = forms.TourImageFormset(instance = self.object, prefix="tour_image")
        context['tour_related_form'] = forms.RelatedTourFormset(instance = self.object,prefix="tour_related")
        context['tour_inclusion_form'] = forms.TourInclusionFormset(instance = self.object,prefix="tour_inclusion")
        context['tour_insight_form'] = forms.TourInsightsFormset(instance = self.object,prefix="tour_insight")
        context['tour_tag_form'] = forms.TourTagFormset(instance = self.object,prefix="tour_tag")
        context['tour_program_form'] = forms.TourProgramFormset(instance = self.object,prefix="tour_program")
        context['tour_question_form'] = forms.TourQuestionsFormset(instance = self.object,prefix="tour_question")    

        return self.render_to_response(context)


    def post(self, request,*args,**kwargs):
        self.object = self.get_object()
        #form_class = self.get_form_class()
        Form = self.get_form_class()
        tour_form = Form(self.request.POST,self.request.FILES,instance = self.object)
        tour_image_form = forms.TourImageFormset(self.request.POST,self.request.FILES,instance = self.object,prefix="tour_image")    
        tour_related_form = forms.RelatedTourFormset(self.request.POST,instance = self.object,prefix="tour_related")
        tour_inclusion_form = forms.TourInclusionFormset(self.request.POST,instance = self.object,prefix="tour_inclusion")
        tour_insight_form = forms.TourInsightsFormset(self.request.POST,instance = self.object,prefix="tour_insight")
        tour_tag_form = forms.TourTagFormset(self.request.POST,instance = self.object,prefix="tour_tag")
        tour_program_form = forms.TourProgramFormset(self.request.POST,instance = self.object,prefix="tour_program")
        tour_question_form = forms.TourQuestionsFormset(self.request.POST,instance = self.object,prefix="tour_question")  

        if (tour_form.is_valid() and tour_image_form.is_valid() and tour_related_form.is_valid() and
            tour_inclusion_form.is_valid() and tour_insight_form.is_valid() and 
            tour_tag_form.is_valid() and tour_program_form.is_valid() and 
            tour_question_form.is_valid()):   
            return self.form_valid(tour_form,tour_image_form,tour_related_form,
                tour_inclusion_form,tour_insight_form,tour_tag_form,
                tour_program_form,tour_question_form
                )
        else:
            return self.form_invalid(tour_form,tour_image_form,tour_related_form,
                tour_inclusion_form,tour_insight_form,tour_tag_form,
                tour_program_form,tour_question_form
                )

    def form_valid(
        self,form,tour_image_form,tour_related_form,tour_inclusion_form,
        tour_insight_form,tour_tag_form,tour_program_form,tour_question_form):
        self.object = form.save()

        tour_image_form.instance = self.object
        tour_image_form.save()

        tour_related_form.instance = self.object
        tour_related_form.save()

        tour_inclusion_form.instance = self.object
        tour_inclusion_form.save()

        tour_insight_form.instance = self.object
        tour_insight_form.save()

        tour_tag_form.instance = self.object
        tour_tag_form.save()

        tour_program_form.instance = self.object
        tour_program_form.save()

        tour_question_form.instance = self.object
        tour_question_form.save()

        return super().form_valid(form) #redirect(self.get_success_url())

    def form_invalid(
        self,form,tour_image_form,tour_related_form,tour_inclusion_form,
        tour_insight_form,tour_tag_form,tour_program_form,tour_question_form):
        context = self.get_context_data()
        context['form'] = form
        context['tour_image_form'] = tour_image_form
        context['tour_related_form'] = tour_related_form
        context['tour_inclusion_form'] = tour_inclusion_form
        context['tour_insight_form'] = tour_insight_form
        context['tour_tag_form'] = tour_tag_form
        context['tour_program_form'] = tour_program_form
        context['tour_question_form'] = tour_question_form
        return self.render_to_response(context)
       
class DeleteTour(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model = models.Tour
    permission_required = 'tour.delete_tour'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete tour'
    success_message = "tour has been successfully deleted!"
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

        print(f'POST IDs {ids} and ID {id}')
     
        if id is not None:
            self.model.objects.get(id=id).delete()
            deleted_ids.append(id)  
            print(f'DELETED ids {deleted_ids}')

        if ids is not None:
            print(f'If IDs {ids}')
            for id in ids:         
                if id is not None:
                    self.model.objects.get(pk=id).delete()
                    deleted_ids.append(id)                           
                else:
                    id_errors.append(f"Object with {id} does not exist")
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)

#TOUR REVIEWS
class ViewTourReviews(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = models.TourReview
    template_name = 'view_tour_reviews.html'
    ordering = ['-review_date']
    paginate_by = 10
    permission_required = 'tour.view_tourreview'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view tour reviews'
    
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
        context["card_title"] = "Tour Review List"
        context['add_url'] = 'tour:add-tour-review'
        context['del_url'] = reverse('tour:delete-tour-reviews')
        context['page_title'] = 'tour reviews'
        return context

class ViewTourReviewDetail(LoginRequiredMixin,DetailView):
    model = models.TourReview
    template_name = 'view_tour_review_detail.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Tour Review Detail"
        context['add_url'] = 'tour:add-tour-review'
        context['del_url'] = reverse('tour:delete-tour-reviews')
        context['page_title'] = 'tour reviews'
        return context

class AddTourReview(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model = models.TourReview
    form_class = forms.TourReviewForm
    template_name = 'add_tour_review.html'  
    success_url = reverse_lazy("tour:view-tour-reviews")
    success_message = "New tour review has been added successfully"
    permission_required = 'tour.add_tourreview'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add tour reviews'
    
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
        context["card_title"] = "Add Tour Review"
        context['save_url'] = 'tour:add-tour-review'
        context['back_url'] = "tour:view-tour-reviews"
        context['form_id'] = 'tour-review-form'
        context['page_title'] = 'tour reviews'
        return context

class UpdateTourReview(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model = models.TourReview
    form_class = forms.TourReviewForm
    template_name = 'add_tour_review.html' 
    success_url = reverse_lazy("tour:view-tour-reviews")
    success_message = "Tour review updated successfully"
    permission_required = 'tour.change_tourreview'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to Tour Reviews'
    extra_context = {
        "card_title": "Update Tour Review",
        'save_url': 'tour:update-tour-review',
        'back_url': "tour:view-tour-reviews",
        'form_id': 'tour-review-form',
        'page_title': 'tour reviews',
    }
    def get_login_url(self):
        login_url = self.login_url or self.request.META.get('HTTP_REFERER')
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)

    """ def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_title"] = "Update Tour Review"
        context['save_url'] = 'tour:update-tour-review'
        context['back_url'] = "tour:view-tour-reviews"
        context['form_id'] = 'tour-review-form'
        context['page_title'] = 'tour reviews'
        return context """

class DeleteTourReview(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model = models.TourReview
    permission_required = 'tour.delete_tourreview'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete tour reviews'
    success_message = "Tour review deleted successfully"
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
        context['message'] = self.success_message
        return JsonResponse(context)


#BOOKING
class ViewBookings(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = models.TourBooking
    template_name = 'view_bookings.html'
    ordering = ['booking_date']
    paginate_by = 10
    permission_required = 'tour.view_tourbooking'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view bookings'
    
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
        context["card_title"] = "Booking List"
        context['add_url'] = 'tour:add-booking'
        context['del_url'] = reverse('tour:delete-bookings')
        context['page_title'] = 'bookings'
        return context

class ViewBookingDetail(LoginRequiredMixin,PermissionRequiredMixin,BaseDetailView):
    model = models.TourBooking
    permission_required = 'tour.change_tourbooking'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view this booking'

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context['customer'] = self.object.customer
            context['tour'] = self.object.tour
            context['booking_date'] = self.object.booking_date
            context['adults'] = self.object.adults
       
            """ context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object """
        #context.update(kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        #msg_data = {"name":self.object.full_name, "email": self.object.email_address, "message":self.object.text_message}
        context = self.get_context_data()
        print(f'message object : {self.object.customer}')
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

class AddBooking(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.TourBooking
    form_class = forms.TourBookingForm
    template_name = 'add_booking.html'  
    success_url = reverse_lazy("tour:view-bookings")
    permission_required = 'tour.add_tourbooking'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add bookings'
    
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
        context["card_title"] = "Add Booking"
        context['save_url'] = 'tour:add-booking'
        context['back_url'] = "tour:view-bookings"
        context['form_id'] = 'booking-form'
        context['page_title'] = 'bookings'
        return context

class UpdateBooking(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = models.TourBooking
    form_class = forms.TourBookingForm
    template_name = 'add_booking.html' 
    success_url = reverse_lazy("tour:view-bookings")
    permission_required = 'tour.change_tourbooking'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to change tour bookings'
    
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
        context["card_title"] = "Update Booking"
        context['save_url'] = 'tour:update-booking'
        context['back_url'] = "tour:view-bookings"
        context['form_id'] = 'booking-form'
        context['page_title'] = 'bookings'
        return context

class DeleteBooking(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = models.TourBooking
    permission_required = 'tour.delete_tourbooking'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete bookings'

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
            self.model.objects.get(pk=id).delete()
            deleted_ids.append(id)  
            print(f'DELETED ids {deleted_ids}')

        if ids is not None:
            for id in ids:         
                if id is not None:
                    self.model.objects.get(pk=id).delete()
                    deleted_ids.append(id)                           
                else:
                    id_errors.append(f"User with {id} does not exist")
        context["data"] = deleted_ids
        context['errors'] = id_errors
        return JsonResponse(context)
