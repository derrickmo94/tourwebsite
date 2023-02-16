from django.db.models import base
from django.urls import include,path
from rest_framework import routers, viewsets
from . import views
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.views import serve

#from durin import views as durin_views
#from yourapp.api.views import LoginView

app_name = "api"

router = routers.DefaultRouter()
router.register(r'app/settings',views.AppSettingsViewSet,basename='app-settings')

#router.register(r'auth/register',views.CustomerRegisterViewSet,basename='customer-register')
#router.register(r'customer/<pk:pk>',views.CustomerRegisterViewSet,basename='customer')

router.register(r'news/subscription',views.NewsletterSubscriptionViewSet,basename="newsletter-subscription")
router.register(r'contact/messages',views.ContactMessageViewSet,basename="contact")
router.register(r'customer/type',views.CustomerTypeViewSet,basename="customer-type")


router.register(r'tour/destinations',views.TourDestinationViewSet, basename="tour-destination-list")
router.register(r'tour/destinations/<slug:destination_slug>',views.TourDestinationViewSet, basename="tour-destination-detail")

router.register(r'tour/categories',views.TourCategoryViewSet, basename="tour-category-list")
router.register(r'tour/categories/<slug:category_slug>',views.TourCategoryViewSet,basename="tour-category-detail")

router.register(r'blog/categories',views.BlogCategoryViewSet, basename="blog-category-list")
router.register(r'blog/categories/<slug:blog_category_slug>',views.BlogCategoryViewSet, basename="blog-category-detail")

router.register(r'blog/articles',views.BlogArticlesViewSet, basename="article-list")
router.register(r'blog/articles/<slug:article_slug>',views.BlogArticlesViewSet, basename="article-detail")

router.register(r'tour/tours',views.ToursViewSet, basename="tour-list")
router.register(r'tour/tours/<slug:tour_slug>',views.ToursViewSet, basename="tour-detail")

router.register(r'tour/review', views.ReviewTourViewSet)

router.register(r'tour/book',views.BookTourViewset, basename="book-tour")
#router.register(r'tour/tours/category/<slug:category_slug>',views.TourViewSet, basename="destination-detail")
#router.register(r'tour/tours/destination/<slug:destination_slug>',views.TourViewSet, basename="category-detail")


urlpatterns = [
    #path('',serve,kwargs={'path':'index.html'}),
    path('',TemplateView.as_view(template_name="home.html"),name="base"),
    path('apiv1/',include(router.urls)),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    #path('apiv1/auth/',include('durin.urls')),
    path('apiv1/auth/',include('djoser.urls')),
    path('apiv1/auth/',include('djoser.urls.authtoken')),
    path('apiv1/auth/',include('djoser.urls.jwt')),
    
] 