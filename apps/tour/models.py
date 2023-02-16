from apps.user.models import CustomerUserProfile
from django.db import models
from datetime import datetime, date
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

#assert __import__(CustomerUserProfile) is not None,("A custom User model representing customers must be imported")


# TOUR DESTINATION MODEL
class TourDestination(models.Model):
    STATUS = (
        (True, "Enabled"),
        (False, "Disabled")
    )
    destination_slug = models.SlugField(
        max_length=255, unique=True, null=True, editable=False)
    name = models.CharField("Destination", max_length=100, unique=True)
    country = models.CharField(max_length=255, default="Uganda")
    tag_line = models.CharField(max_length=200, null=True, blank=True)
    tag_text = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        default="system/default.png", upload_to='tour/destinations')
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(choices=STATUS, default=1)

    class Meta:
        verbose_name = _('destination')
        verbose_name_plural = _('destinations')

    def save(self, *args, **kwargs):
        self.destination_slug = slugify(f'{self.country} {self.name}')
        super(TourDestination, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            newimg = (500, 500)
            img.thumbnail(newimg)
            img.save(self.image.path)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tour:update-destination", kwargs={'pk': self.pk})


# TOUR CATEGORY MODEL
class TourCategory(models.Model):
    STATUS = (
        (True, "Enabled"),
        (False, "Disabled")
    )
    category_slug = models.SlugField(
        max_length=255, unique=True, null=True, blank=True, editable=False)
    name = models.CharField("Category", max_length=100, unique=True)
    image = models.ImageField(
        default="system/default.png", upload_to='tour/categories')
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(choices=STATUS, default=1)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def save(self, *args, **kwargs):
        # if not self.category_slug:
        self.category_slug = slugify(self.name)
        super(TourCategory, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            newimg = (500, 500)
            img.thumbnail(newimg)
            img.save(self.image.path)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tour:update-tour-category", kwargs={"pk": self.pk})


# TOUR MODEL
class Tour(models.Model):
    STATUS = (
        (True, "Enabled"),
        (False, "Disabled")
    )
    tour_slug = models.SlugField(
        max_length=255, editable=False, null=True, blank=True, unique=True)
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(
        default="system/default.png", upload_to='tour/tours')
    destination = models.ForeignKey(
        TourDestination, related_name="tours", on_delete=models.PROTECT)
    category = models.ForeignKey(
        TourCategory, related_name="tours", on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    discount = models.IntegerField(null=True, blank=True,help_text=_("discount in percentage e.g 5 or 10"))
    duration = models.IntegerField()
    description = models.TextField()
    reviews = models.BigIntegerField(editable=False, default=0)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0.0, editable=False)
    advertise = models.BooleanField(default=False)
    ad_title = models.CharField("advert title", max_length=50, null=True, blank=True, help_text=_(
        "title tag for the ad e.g SALE or PROMOTION. etc "))
    ad_name = models.CharField("advert name", max_length=255, null=True, blank=True, help_text=_(
        "the name of the tour add e.g sale of the week, or week discount"))
    ad_description = models.TextField("advert description", null=True, blank=True, help_text=_(
        "a decription of the advertisment or promotion with probably more details with regard to the ad or promotion offer"))
    new_tag = models.CharField(max_length=10, editable=False, default="New")
    added = models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True,null=True)
    status = models.BooleanField("Status", choices=STATUS, default=1)
    discounted_price = models.DecimalField(decimal_places=2, max_digits=15,null=True,blank=True,editable=False)

    class Meta:
        verbose_name = 'tour'
        verbose_name_plural = 'tours'
        ordering = ['-added']

    def save(self, *args, **kwargs):
        super(Tour, self).save(*args, **kwargs)
        if not self.tour_slug:
            self.tour_slug = slugify(self.name)
        if self.discount is not None and self.discount > 0:
            self.discounted_price =  self.price - (self.price*self.discount/100)
        else:
            self.discounted_price = None
        
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            newimg = (500, 500)
            img.thumbnail(newimg)
            img.save(self.image.path)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tour:update-tour", kwargs={"pk": self.pk})


class TourReview(models.Model):
    STATUS = (
        (True, "Published"),
        (False, "Un Published")
    )
    tour = models.ForeignKey(
        Tour, related_name="tour_reviews", on_delete=models.CASCADE)
    customer = models.ForeignKey(
        CustomerUserProfile, related_name="tour_reviews", to_field="user_id", on_delete=models.SET_NULL,null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1,)
    review = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True, choices=STATUS)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')

        ordering = ['-review_date']

    def __str__(self):
        return f'{self.tour} review'

    def get_absolute_url(self):
        return reverse("tour:update-tour-review", kwargs={"pk": self.pk})

    def get_absolute_detail_url(self):
        return reverse("tour:view-tour-review-detail", kwargs={"pk": self.pk})


# RELATED TOUR MODEL
class RelatedTour(models.Model):
    tour = models.ForeignKey(Tour, related_name="related_tours",
        on_delete=models.CASCADE, null=True, blank=True)
    related_tour = models.OneToOneField(
        Tour, on_delete=models.CASCADE, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = _('related tour')
        verbose_name_plural = _('related tours')

    def __str__(self):
        return self.related_tour

    def get_tour(self):
        return self.related_tour.name


# TOUR TAG MODEL
class TourTag(models.Model):
    tag = models.CharField(max_length=100, null=True, blank=True)
    tour = models.ForeignKey(
        Tour, related_name="tour_tags", on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.tag


# TOUR IMAGE MODEL
class TourImage(models.Model):
    image = models.ImageField(
        default='system/default.png', upload_to="tour/tours", null=True, blank=True)
    tour = models.ForeignKey(
        Tour, related_name="tour_images", on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.image


# TOUR QUESTION
class TourQuestion(models.Model):
    question = models.CharField(max_length=255, null=True, blank=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    tour = models.ForeignKey(
        Tour, related_name="tour_questions", on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.question


# TOUR PROGRAM MODEL
class TourProgram(models.Model):
    program = models.CharField(max_length=255, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tour = models.ForeignKey(
        Tour, related_name="tour_programs", on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _('program')
        verbose_name_plural = _('programs')

    def __str__(self):
        return self.program


# TOUR INCLUSION MODEL
class TourInclusion(models.Model):
    inclusion = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tour = models.ForeignKey(
        Tour, related_name="tour_inclusions", on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _('inclusion')
        verbose_name_plural = _('inclusions')

    def __str__(self):
        return self.inclusion


# TOUR INSIGHT MODEL
class TourInsight(models.Model):
    insight = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tour = models.ForeignKey(
        Tour, related_name="tour_insights", on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = _('insight')
        verbose_name_plural = _('insights')

    def __str__(self):
        return self.insight


# TOUR BOOKING MODEL
class TourBooking(models.Model):
    STATUS = (
        (True, "Enabled"),
        (False, "Disabled")
    )
    tour = models.ForeignKey(Tour, related_name="tour_bookings", on_delete=models.RESTRICT, null=True)
    customer = models.ForeignKey(CustomerUserProfile, to_field='user_id', related_name="tour_bookings", on_delete=models.RESTRICT)
    booking_date = models.DateTimeField(auto_now_add=True)
    arrival_date = models.DateField(default=timezone.now)
    tour_start_date = models.DateField(default= timezone.now)
    pickup_address = models.CharField(max_length=255, null=True, blank=True)
    dropoff_address = models.CharField(max_length=255, default="")
    adults = models.IntegerField("Number of Adults", default=0)
    children = models.IntegerField("Number of children", default=0)
    extra_info = models.TextField(null=True, blank=True)
    status = models.BooleanField(_('Status'),choices=STATUS,default=0)

    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')

    def get_absolute_url(self):
        return reverse("tour:view-booking-detail", kwargs={"pk": self.pk})