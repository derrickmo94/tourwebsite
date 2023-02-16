from django.contrib.auth.models import Permission, PermissionsMixin
from django.core.files.base import equals_lf
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http.response import Http404
from django.shortcuts import render
from rest_framework import response, serializers, viewsets
from . import serializers as szers
from apps.user import models as user_mds
from apps.blog import models as blog_mds
from apps.tour import models as tour_mds
from apps.system import models as system_mds
from rest_framework.parsers import JSONParser,MultiPartParser
from rest_framework.pagination import PageLink, PageNumberPagination
from rest_framework import filters
from rest_framework.response import Response
#from knox.models import AuthToken
from rest_framework import status
from django.contrib.auth import get_user_model
from collections import OrderedDict
from rest_framework.permissions import AllowAny

User = get_user_model()

class StandardPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 1000
    #display_page_controls = True
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            #('next', self.get_next_link()),
            #('previous', self.get_previous_link()),
            ('page_size',self.get_page_size(self.request)),
            ('page_urls',self.get_html_context()),
            ('results', data)
        ]))

class DestinationPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'
    max_page_size = 1000
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size',self.get_page_size(self.request)),
            ('page_urls',self.get_html_context()),
            ('results', data)
        ]))

class TourPagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'page'
    max_page_size = 1000
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size',self.get_page_size(self.request)),
            ('page_urls',self.get_html_context()),
            ('results', data)
        ]))

class ArticlePagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 1000
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size',self.get_page_size(self.request)),
            ('page_urls',self.get_html_context()),
            ('results', data)
        ]))

class MultiTourSerializerMixin(object): 
    """This Mixin provides dynamic serializers best on the request action"""
    def get_serializer_class(self,*args, **kwargs):         
        if self.action == "retrieve":
            if hasattr(self,'retrieve'):
                return self.get_detail_serializer_class()
        if self.action == "list":
            if hasattr(self,'list'):      
                return self.get_list_serializer_class()
        if self.action == "create":
            if hasattr(self,'create'):      
                return self.get_create_serializer_class()
        return self.get_default_serializer_class()

    def get_default_serializer_class(self):
        """Returns the value of serializer_class attribute as the default serializer class"""

        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute as default,"
            "or override the `get_default_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.serializer_class

    def get_detail_serializer_class(self):
        """Returns a serializer class used to serialize a single object instance"""

        if hasattr(self,"detail_serializer_class"):
            assert self.detail_serializer_class is not None, (
                "'%s' should either include a `detail_serializer_class` attribute,"
                "or override the `get_detail_serializer_class()` method."
                % self.__class__.__name__
            )
            if self.detail_serializer_class is not None:
                return self.detail_serializer_class
        return self.get_default_serializer_class()

    def get_list_serializer_class(self):
        """Returns a serializer class used to serialize a collection [list] of objects"""

        if hasattr(self,"list_serializer_class"):
            assert self.list_serializer_class is not None, (
                "'%s' should either include a `list_serializer_class` attribute,"
                "or override the `get_list_serializer_class()` method."
                % self.__class__.__name__
            )
            if self.list_serializer_class is not None:
                return self.list_serializer_class
        return self.get_default_serializer_class()

    def get_create_serializer_class(self):
        """Returns a serializer class used to serialize an object instance that has been created"""

        if hasattr(self,"create_serializer_class"):
            assert self.create_serializer_class is not None, (
                "'%s' should either include a `create_serializer_class` attribute,"
                "or override the `get_create_serializer_class()` method."
                % self.__class__.__name__
            )
            if self.create_serializer_class is not None:
                return self.create_serializer_class
            return self.get_default_serializer_class()

""" class MultiSerializerMixin: 0795098398
    serializer_classes ={
        'list':szers.ToursSerializer,
        'retrieve': szers.TourSerializer
    }
    default = szers.ToursSerializer
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action,self.default) """


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = system_mds.ContactMessage.objects.all()
    serializer_class = szers.ContactMessageSerializer
    permission_classes = [AllowAny]


class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = system_mds.NewsletterSubscription.objects.all()
    serializer_class = szers.NewsletterSubscriptionSerializer
    permission_classes = [AllowAny]


class CustomerTypeViewSet(viewsets.ModelViewSet):
    queryset = user_mds.CustomerType.objects.filter(status=True)
    serializer_class = szers.CustomerUserTypeSerializer


class AppSettingsViewSet(viewsets.ModelViewSet):
    queryset = system_mds.Settings.objects.all()
    serializer_class = szers.AppSettingSerializer
    

class TourDestinationViewSet(viewsets.ModelViewSet):
    queryset = tour_mds.TourDestination.objects.annotate(num_tours = Count('tours')).order_by('name').all() #filter(status=True)
    serializer_class = szers.TourDestinationSerializer
    pagination_class = DestinationPagination
    lookup_field ='destination_slug'

    def paginate_queryset(self, queryset):
        paging = self.request.query_params.get('g')
        if paging is not None and paging == "true":   
            return self.paginator.paginate_queryset(queryset, self.request, view=self)      
        elif paging is not None and paging == "false": 
            None
        else:
            return None

    def get_queryset(self):
        queryset = self.queryset
        latest =  self.request.query_params.get('ltst')
        
        if latest is not None:
            queryset = queryset.filter(status=True)[:int(latest)]
            return queryset
        else:
            queryset = queryset.filter(status=True,)
            return queryset


class TourCategoryViewSet(viewsets.ModelViewSet):
    queryset = tour_mds.TourCategory.objects.annotate(num_tours = Count('tours')).order_by('name').filter(status=True)
    serializer_class = szers.TourCategorySerializer
    #pagination_class = StandardPagination
    lookup_field ='category_slug'


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = blog_mds.BlogCategory.objects.all().order_by('name').filter(status=True)
    serializer_class = szers.BlogCategorySerializer
    lookup_field = 'blog_category_slug'


class BlogArticlesViewSet(viewsets.ModelViewSet):
    queryset = blog_mds.BlogArticle.objects.select_related('category').order_by('-publish_date').all()#filter(status=True)
    serializer_class = szers.BlogArticleSerializer
    lookup_field = 'article_slug'
    pagination_class = ArticlePagination

    def paginate_queryset(self, queryset):
        paging = self.request.query_params.get('g')
        if paging is not None and paging == "true":   
            return self.paginator.paginate_queryset(queryset, self.request, view=self)      
        elif paging is not None and paging == "false":
            return  None
        else:
            return None
    
    def get_queryset(self):
        queryset = self.queryset 
        category = self.request.query_params.get('category')
        category_name = self.request.query_params.get('category_name')
        latest =  self.request.query_params.get('ltst')

        if category is not None:
            queryset = queryset.filter(category__blog_category_slug=category,status=True)
            return queryset
        elif category_name is not None:
            queryset = queryset.filter(category__name=category_name,status=True)
            return queryset
        elif latest is not None:
            queryset = queryset.filter(status=True)[:int(latest)]
            return queryset
        else:
            return queryset


class ToursViewSet(MultiTourSerializerMixin,viewsets.ModelViewSet):
    queryset =  tour_mds.Tour.objects.all()
    list_serializer_class = szers.ToursSerializer
    #detail_serializer_class = szers.TourSerializer
    serializer_class = szers.TourSerializer
    pagination_class = TourPagination

    lookup_field = 'tour_slug'
    #filter_backends = [filters.SearchFilter]
    #search_fields =['name','tour_slug']
    def paginate_queryset(self, queryset):
        paging = self.request.query_params.get('g')
        if paging is not None and  paging == "true":   
                return self.paginator.paginate_queryset(queryset, self.request, view=self)      
        elif paging is not None and paging == "false":
                return  None
        else:
            return None #self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_queryset(self):
        category = self.request.query_params.get('category')
        destination = self.request.query_params.get('destination')
        latest =  self.request.query_params.get('ltst')
        queryset = self.queryset
        
        if category is not None:
            queryset = queryset.filter(status=True,category__category_slug=category)
            return queryset
        elif destination is not None:
            queryset = queryset.filter(status=True,destination__destination_slug=destination)
            return queryset
        elif latest is not None:
            queryset = queryset.filter(status=True)[:int(latest)]
            return queryset
        else:
            queryset = queryset.filter(status=True,)
            return queryset


class ReviewTourViewSet(MultiTourSerializerMixin, viewsets.ModelViewSet):
    queryset = tour_mds.TourReview.objects.all()
    create_serializer_class = szers.ReviewTourSerializer
    serializer_class = szers.TourReviewSerializer

    def get_queryset(self):
        queryset = self.queryset
        tour_param = self.request.query_params.get('tour')
        if tour_param is not None:
            queryset = queryset.filter(tour__pk = int(tour_param), status = True)
            return queryset
        else:
            queryset = queryset.filter(status = True)
            return queryset


class BookTourViewset(MultiTourSerializerMixin,viewsets.ModelViewSet):
    queryset = tour_mds.TourBooking.objects.all()
    list_serializer_class = szers.TourBookingsSerialiazer
    detail_serializer_class = szers.TourBookingSerialiazer
    create_serializer_class = szers.TourBookSerialiazer
    default_serializer_class = szers.TourBookingsSerialiazer
    pagination_class = TourPagination

    def paginate_queryset(self, queryset):
        paging = self.request.query_params.get('g')
        if paging is not None and  paging == "true":   
                return self.paginator.paginate_queryset(queryset, self.request, view=self)      
        elif paging is not None and paging == "false":
                return None
        else:
            return None #self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_queryset(self):
        queryset = self.queryset.filter(customer = self.request.user.id)
        """ status = self.request.query_params.get('st')
        if status is not None:
            queryset = self.queryset.filter(customer = self.request.user)
            return queryset
        else:
            return self.queryset """
        return queryset
