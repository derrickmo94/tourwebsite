from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
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


#BLOG CATEGORY
class ViewBlogCategories(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = models.BlogCategory
    template_name = 'view_blog_categories.html'
    ordering = ['name']
    paginate_by = 10
    permission_required = 'blog.view_blogcategory'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view blog categories'
    
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
        context['add_url'] = 'blog:add-blog-category'
        context['del_url'] = reverse('blog:delete-blog-categorys')
        context['page_title'] = 'blog categories'
        return context

class AddBlogCategory(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.BlogCategory
    form_class = forms.BlogCategoryForm
    template_name = 'add_blog_category.html'  
    success_url = reverse_lazy("blog:view-blog-categories")
    permission_required = 'blog.add_blogcategory'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add blog categories'
    
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
        context['save_url'] = 'blog:add-blog-category'
        context['back_url'] = "blog:view-blog-categories"
        context['form_id'] = 'blog-category-form'
        context['page_title'] = 'blog categories'
        return context

class UpdateBlogCategory(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = models.BlogCategory
    form_class = forms.BlogCategoryForm
    template_name = 'add_blog_category.html' 
    success_url = reverse_lazy("blog:view-blog-categories")
    permission_required = 'blog.change_blogcategory'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add blog categories'
    
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
        context['save_url'] = 'blog:update-blog-category'
        context['back_url'] = "blog:view-blog-categories"
        context['form_id'] = 'blog-category-form'
        context['page_title'] = 'blog categories'
        return context

class DeleteBlogCategory(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = models.BlogCategory
    permission_required = 'blog.delete_blogcategory'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete blog categories'

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


#BLOG ARTICLE
class ViewBlogArticles(LoginRequiredMixin,PermissionRequiredMixin,ListView):  
    model = models.BlogArticle
    template_name = 'view_blog_articles.html'
    ordering = ['article_title']
    paginate_by = 10
    permission_required = 'blog.view_blogarticle'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to view blog articles'
    
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
        context["card_title"] = "Article List"
        context['add_url'] = 'blog:add-blog-article'
        context['del_url'] = reverse('blog:delete-blog-articles')
        context['page_title'] = 'blog articles'
        return context

class AddBlogArticle(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = models.BlogArticle
    form_class = forms.BlogArticleForm
    template_name = 'add_blog_article.html'  
    success_url = reverse_lazy("blog:view-blog-articles")
    permission_required = 'blog.add_blogarticle'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to add blog articles'
    
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
        context["card_title"] = "Add Article"
        context['save_url'] = 'blog:add-blog-article'
        context['back_url'] = "blog:view-blog-articles"
        context['form_id'] = 'blog-article-form'
        context['page_title'] = 'blog articles'
        return context

class UpdateBlogArticle(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = models.BlogArticle
    form_class = forms.BlogArticleForm
    template_name = 'add_blog_article.html' 
    success_url = reverse_lazy("blog:view-blog-articles")
    permission_required = 'blog.change_blogarticle'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to  make changes to blog articles'
    
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
        context["card_title"] = "Update Article"
        context['save_url'] = 'blog:update-blog-article'
        context['back_url'] = "blog:view-blog-articles"
        context['form_id'] = 'blog-article-form'
        context['page_title'] = 'blog articles'
        return context

class DeleteBlogArticle(LoginRequiredMixin,DeleteView):
    model = models.BlogArticle
    permission_required = 'blog.delete_blogarticle'
    permission_denied_message = '<strong>Access denied</strong> You don\'t have permission to delete blog articles'

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
