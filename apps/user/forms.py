from django import forms #import ModelForm, CheckboxSelectMultiple,MultipleChoiceField, forms, widgets
from django.contrib.auth.models import Group
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import hashers as hashalgo
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomReadOnlyPasswordHashWidget(auth_forms.ReadOnlyPasswordHashWidget):
    #template_name = 'auth/widgets/read_only_password_hash.html'
    #read_only = True

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith( hashalgo.UNUSABLE_PASSWORD_PREFIX):
            summary.append({'label': _("No password set.")})
        else:
            try:
                hasher = hashalgo.identify_hasher(value)
            except ValueError:
                summary.append({'label': _("Invalid password format or unknown hashing algorithm.")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({'label': ("********")})
        context['summary'] = summary
        return context


class CustomReadOnlyPasswordHashField(auth_forms.ReadOnlyPasswordHashField):
    widget = CustomReadOnlyPasswordHashWidget

class FormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        #self.form_class='form-horizontal'
        self.label_class='text-start text-md-end'
        #self.field_class='col'
        self.template = 'user/bootstrap4/table_inline_formset.html'


class AdminLoginForm(auth_forms.AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """
    error_messages = {
        **auth_forms.AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct %(username)s and password for a staff "
            "account. Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )


class UserGroupForm(forms.ModelForm):   
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions':forms.CheckboxSelectMultiple()
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='user-group-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'


class UserForm(auth_forms.UserCreationForm):    
    class Meta:
        model = User
        fields = ["image","username","first_name","last_name","email","phone_number","groups","is_superuser","is_staff","is_active"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id='user-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 col-form-label text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'
        self.helper.form_tag = False

    def clean(self):
        self.cleaned_data = super(UserForm,self).clean() 
        self.cleaned_data["is_staff"] = True
        #self.instance.is_staff = True
        return self.cleaned_data

class UserChangeForm(auth_forms.UserChangeForm):   
    password = CustomReadOnlyPasswordHashField(
        help_text= (      
            'Click &nbsp;<a class="text-primary" href="{}">this link to change the user password </a>'
            '&nbsp; since raw passwords are not stored hence no way to see it from here.'
        )
    ) 
    class Meta:
        model = User
        fields = ["image","username","first_name","last_name","email","groups","is_superuser","is_staff","is_active","password"]

    """ def clean(self):
        cleaned_data = super().clean()
        is_administrator = cleaned_data.get("is_administrator")
        title = cleaned_data.get("title")

        if is_administrator and title is None:
            # Only do something if both fields are valid so far.
            error = "You must provide an administrator title or role if administartor status is true"
            self.add_error('title',error) """
            

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('password/user')
        else:
            password.help_text = password.help_text.format('passwor/user') 
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

        self.helper = FormHelper()
        self.helper.form_id='user-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'
        self.helper.form_tag = False

    def clean(self):
        self.cleaned_data = super(UserChangeForm,self).clean() 
        self.cleaned_data["is_staff"] = True
        #self.instance.is_staff = True
        return self.cleaned_data

class UserAdminPasswordChangeForm(auth_forms.AdminPasswordChangeForm):    
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='change-user-password-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = models.AdminUserProfile
        exclude = ['is_admin','user']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='admin-user-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'
        self.helper.form_tag = False


class CustomerUserVersionUserForm(auth_forms.UserCreationForm):    
    class Meta:
        model = User
        fields = ["image","username","first_name","last_name","email","is_active"]
         
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id='user-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 col-form-label text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'
        self.helper.layout = Layout(          
        )
        self.helper.form_tag = False
        #self.disable_csrf = True

    def clean(self):
        self.cleaned_data = super(CustomerUserVersionUserForm,self).clean() 
        self.cleaned_data["is_staff"] = False
        return self.cleaned_data

class CustomerUserChangeForm(auth_forms.UserChangeForm):   
    password = CustomReadOnlyPasswordHashField(
        help_text= (      
            'Click &nbsp;<a class="text-primary" href="{}">this link to change the user password </a>'
            '&nbsp; since raw passwords are not stored hence no way to see it from here.'
        )
    ) 
    class Meta:
        model = User
        fields = ["image","username","first_name","last_name","email","is_active",'password']
            
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('password/user')
        else:
            password.help_text = password.help_text.format('passwor/user') 
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

        self.helper = FormHelper()
        self.helper.form_id='user-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'
        self.helper.form_tag = False

    def clean(self):
        self.cleaned_data = super(CustomerUserChangeForm,self).clean() 
        self.cleaned_data["is_staff"] = False
        return self.cleaned_data

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = models.CustomerUserProfile
        fields = ['customer_type']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='customer-user-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'
        self.helper.form_tag = False
        self.disable_csrf = True

class CustomerTypeForm(forms.ModelForm):
    class Meta:
        model = models.CustomerType
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='customer-type-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'