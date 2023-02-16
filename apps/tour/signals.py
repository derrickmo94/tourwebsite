from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models as mds

@receiver(post_save,sender = mds.TourReview)
def tour_average_rating(sender,instance,created,**kwargs):
    def get_avg_rating(ratings):
        sum = 0
        if len(ratings) > 0:
            for rating in ratings:
                sum = sum + rating['rating']
            #print(f'SUM: {sum}')
            #print(f'SAVG VAL: {sum/int(len(ratings))}')
            return (sum/int(len(ratings)))
        else:
            return 0
    parent = instance.tour
    tour_reviews = sender.objects.filter(tour = parent).values('rating')
    #print(f'AVERAGE RATING: {tour_ratings}')
    parent.reviews = len(tour_reviews)
    parent.rating = get_avg_rating(tour_reviews)
    parent.save()
    #print(f'AVERAGE RATING 2: {tour_reviews["avg_rating"]}')