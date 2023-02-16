from django.urls import path
from . import views as tour_views

app_name = "tour"
urlpatterns = [
    path('tour/destinations',tour_views.ViewTourDestinations.as_view(),name='view-destinations'),
    path('tour/destination/add',tour_views.AddTourDestination.as_view(),name="add-destination"),
    path('tour/destination/<int:pk>/',tour_views.UpdateTourDestination.as_view(),name='update-destination'),
    path('tour/destination/<int:pk>/delete/',tour_views.DeleteTourDestination.as_view(),name='delete-destination'),
    path('tour/destination/delete/',tour_views.DeleteTourDestination.as_view(),name='delete-destinations'),

    path('tour/categories',tour_views.ViewTourCategories.as_view(),name='view-tour-categories'),
    path('tour/category/add',tour_views.AddTourCategory.as_view(),name='add-tour-category'),
    path('tour/category/<int:pk>/',tour_views.UpdateTourCategory.as_view(),name='update-tour-category'),
    path('tour/category/<int:pk>/delete/',tour_views.DeleteTourCategory.as_view(),name='delete-tour-category'),
    path('tour/category/delete/',tour_views.DeleteTourCategory.as_view(),name='delete-tour-categorys'),

    path('tours',tour_views.ViewTours.as_view(),name='view-tours'),
    path('tour/add',tour_views.AddTour.as_view(),name='add-tour'),
    path('tour/<int:pk>/',tour_views.UpdateTour.as_view(),name='update-tour'),
    path('tour/<int:pk>/delete',tour_views.DeleteTour.as_view(),name='delete-tour'),
    path('tour/delete',tour_views.DeleteTour.as_view(),name='delete-tours'),

    path('tour/reviews',tour_views.ViewTourReviews.as_view(),name='view-tour-reviews'),
    path('tour/review-detail/<int:pk>/',tour_views.ViewTourReviewDetail.as_view(),name='view-tour-review-detail'),
    path('tour/add-review',tour_views.AddTourReview.as_view(),name='add-tour-review'),
    path('tour/review/<int:pk>/',tour_views.UpdateTourReview.as_view(),name='update-tour-review'),
    path('tour/review/<int:pk>/delete',tour_views.DeleteTourReview.as_view(),name='delete-tour-review'),
    path('tour/review/delete',tour_views.DeleteTourReview.as_view(),name='delete-tour-reviews'),

    path('bookings',tour_views.ViewBookings.as_view(),name='view-bookings'),
    path('booking/add',tour_views.AddBooking.as_view(),name='add-booking'),
    path('booking/<int:pk>/',tour_views.UpdateBooking.as_view(),name='update-booking'),
    path('booking/<int:pk>/detail',tour_views.ViewBookingDetail.as_view(),name='view-booking-detail'),
    path('booking/<int:pk>/delete',tour_views.DeleteBooking.as_view(),name='delete-booking'),
    path('booking/delete',tour_views.DeleteBooking.as_view(),name='delete-bookings'),
]