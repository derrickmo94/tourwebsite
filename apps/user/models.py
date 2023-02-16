from django.db import models
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.urls import reverse
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


#USER PROFILE MODEL
class User(AbstractUser):
    image = models.ImageField(
        default='system/default.png', upload_to='profile_image')
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.IntegerField(unique=True, blank=True, null=True)
    group = None
    groups = models.ForeignKey(
        Group,
        verbose_name=_('group'),
        blank=True,
        null=True,
        help_text=_(
            'The group this user belongs to. A user will get all permissions '
            'granted to each of their group.'
        ),
        related_name="user_set",
        related_query_name="user",
        on_delete=models.SET_NULL
    )

    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = False
        #swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        super(User,self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        newimg = (500, 500)
        img.thumbnail(newimg)
        img.save(self.image.path)
        

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_absolute_url(self):
        return reverse("user:update-user", kwargs={"pk": self.pk})

    def get_absolute_customer_url(self):
        return reverse("user:update-customer", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("user:delete-user", kwargs={"pk": self.pk})

#ADMIN USER PROFILE
class AdminUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="admin_user_profile",related_query_name="admin_user_profile")
    is_admin = models.BooleanField(
        _('admin status'), default=True, editable=False)
    class Meta:
        verbose_name = _("admin user")
        verbose_name_plural = _("admin users")
    
    def __str__(self):
        return f'{self.user.username}'

#CUSTOMER USER TYPE
class CustomerType(models.Model):
    STATUS = (
        (True, "Enabled"),
        (False, "Disabled")
    )
    #type_selector_text = models.CharField(_("type selector text"), max_length=255)
    type_name = models.CharField(_("customer type"), max_length=255)
    status = models.BooleanField(choices=STATUS, default=1)
    class Meta:
        verbose_name = _('customer type')
        verbose_name_plural = _('customer types')

    def __str__(self):
        return f'{self.type_name}'

    def get_absolute_url(self):
        return reverse("user:update-customer-type", kwargs={"pk": self.pk})  

#CUSTOMER USER PROFILE
class CustomerUserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="customer_user_profile", related_query_name="customer_user_profile", on_delete=models.CASCADE)
    is_customer = models.BooleanField(_('customer status'), default=True, editable=False)
    customer_type = models.ForeignKey(CustomerType, verbose_name="customer type", related_name="customer_user_profiles",on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name = _('customer user')
        verbose_name_plural = _('customer users')


    def __str__(self):
        return f'{self.user.username} profile'

    def get_absolute_url(self):
        return reverse("user:update-customer", kwargs={"pk": self.user.pk})