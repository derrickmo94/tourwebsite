from apps.user.models import AdminUserProfile
from django.db import models
from datetime import datetime, date
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

#assert __import__(AdminUserProfile) is not None,("A User model must be imported")


#CONTACT MESSAGE
class ContactMessage(models.Model):
    full_name = models.CharField(_('name'), max_length=255)
    email_address = models.EmailField(_('email_address'))
    date_sent = models.DateTimeField(auto_now_add=True)
    text_message = models.TextField(_('message'))

    class Meta:
        verbose_name = _('contact message')
        verbose_name_plural = _('contact messages')

    def __str__(self):
        return f'contact message email: {self.email_address}'

    def get_absolute_url(self):
        return reverse("system:contact-message-detail", kwargs={"pk": self.pk})


#NEWSLETTER SUBSCRIPTION MODEL
class NewsletterSubscription(models.Model):
    full_name = models.CharField(_('name'), max_length=255)
    email_address = models.EmailField(_('email_address'))
    subscription_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('newsletter subscription')
        verbose_name_plural = _('newsletter subscriptions')

    def __str__(self):
        return f'newsletter subscription email: {self.email_address}'


# SETTINGS MODEL
class Settings(models.Model):
    STATUS = (
        (True, "Enabled"),
        (False, "Disabled")
    )
    company_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    logo = models.ImageField(default='system/default.png',
                             upload_to='system/logos', null=True, blank=True)
    icon = models.ImageField(default='system/default.png',
                             upload_to='system/logos', null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)
    phone_message = models.TextField(max_length=100, blank=True, null=True,
                                     help_text="The message that will be added besides a contact phone number above")
    email = models.CharField("Email Address", max_length=255)
    email_message = models.TextField(max_length=100, blank=True, null=True,
                                     help_text="The message that will be added besides an email address above")
    fax = models.CharField("Fax Number", max_length=255, null=True, blank=True)
    address_code = models.IntegerField("zip code/box number", unique=True)
    physical_address = models.CharField(max_length=255)
    physical_address_message = models.TextField(
        max_length=100, blank=True, null=True, help_text="The message that will be added besides the physical address above")
    employee_number = models.BigIntegerField(default=0)
    launch_time = models.DateField(auto_created=True, editable=True)
    tour_bookings = models.IntegerField(default=230, editable=False)
    #managment_user = models.ForeignKey(ManagmentUser,on_delete=models.DO_NOTHING)
    status = models.BooleanField(choices=STATUS, default=True)

    class Meta:
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        logo = Image.open(self.logo.path)
        icon = Image.open(self.icon.path)
        if logo.height > 50 or logo.width > 50:
            l_newimg = (500, 500)
            logo.thumbnail(l_newimg)
            logo.save(self.logo.path)

        if icon.height > 50 or icon.width > 50:
            i_newimg = (50, 50)
            icon.thumbnail(i_newimg)
            icon.save(self.icon.path)

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return reverse("system:update-system-setting", kwargs={"pk": self.pk})


class CompanyStatement(models.Model):
    image = models.ImageField(default="system/default.png",
                              upload_to="system/company_statement", null=True, blank=True)
    statement_title = models.CharField(max_length=100, null=True, blank=True, help_text=_(
        "This can be the vision,mision,goal,purpose,etc of the company and any thing in that line"))
    statement = models.TextField(max_length=2000, null=True, blank=True, help_text=_(
        "This is the respective vision, or mission statement "))
    company_settings = models.ForeignKey(
        Settings, related_name="company_statements", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('company statement')
        verbose_name_plural = _('company statements')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)

        if image.height > 500 or image.width > 500:
            newimg = (500, 500)
            image.thumbnail(newimg)
            image.save(self.image.path)

    def __str__(self):
        return self.statement_title


class CompanyImage(models.Model):
    image = models.ImageField(
        default="system/default.png", upload_to="system/company", null=True, blank=True)
    company_settings = models.ForeignKey(
        Settings, related_name="company_images", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('company image')
        verbose_name_plural = _('company images')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        c_image = Image.open(self.image.path)

        # if c_image.height > 50 or c_image.width > 50:
        c_newimg = (500, 400)
        c_image.thumbnail(c_newimg)
        c_image.save(self.image.path)


class CompanyAdmin(models.Model):
    user = models.OneToOneField(AdminUserProfile, on_delete=models.CASCADE, help_text=_(
        "A user profile / user to be designated as part of the company administrators e.g Board member,CEO,Head of a department,etc"))
    company_settings = models.ForeignKey(
        Settings, related_name="company_admins", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, help_text=_(
        "The respective title/position of the user in the company e.g CEO,Operations Manager,Head of advertisment, etc"))
    is_company_admin = models.BooleanField(default=True, editable=False)

    class Meta:
        verbose_name = _('company admin')
        verbose_name_plural = _('company admins')


class SocialMedia(models.Model):
    SOCIAL_ICONS = (
        ('fab fa-facebook', 'facebook'),
        ('fab fa-twitter-square', 'twitter'),
        ('fab fa-instagram', 'instagram'),
        ('fab fa-linkedin', 'linkedin'),
        ('fab fa-snapchat', 'snapchat'),
        ('fab fa-tiktok', 'tiktok'),
        ('fab fa-whatsapp', 'whatsapp'),
    )
    social_media_icon = models.CharField(
        max_length=255, choices=SOCIAL_ICONS, null=True, blank=True)
    social_media_handle = models.CharField(
        _('social media handle / profile'), max_length=255, null=True, blank=True)
    company_settings = models.ForeignKey(
        Settings, related_name="company_social_medias", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('social media')
        verbose_name_plural = _('social media')