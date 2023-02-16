from django import forms 
from django.core.exceptions import ValidationError
from . import models
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class FormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        #self.form_class='form-horizontal'
        self.label_class='text-start text-md-end'
        #self.field_class='col'
        self.template = 'system/bootstrap4/table_inline_formset.html'

class SystemSettingsForm(forms.ModelForm):    
    class Meta:
        model = models.Settings
        fields = '__all__' 
        widgets = { 
            'description':forms.Textarea(attrs={'rows':2}),
            'meta_description':forms.Textarea(attrs={'rows':2}),
            'meta_keywords':forms.Textarea(attrs={'rows':2}),
            'phone_message':forms.Textarea(attrs={'rows':2}),
            'email_message':forms.Textarea(attrs={'rows':2}),
            'physical_address':forms.Textarea(attrs={'rows':2}),
            'physical_address_message':forms.Textarea(attrs={'rows':2}),

            }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='settings-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'
        self.helper.form_tag = False


class CompanyStatementForm(forms.ModelForm):
    class Meta:
        model = models.CompanyStatement
        fields = '__all__'
        widgets = { 'statement':forms.Textarea(attrs={'rows':2})}
CompanyStatementFormset = forms.inlineformset_factory(models.Settings, models.CompanyStatement,form=CompanyStatementForm,can_delete=True,extra=1)


class CompanyImageForm(forms.ModelForm):
    class Meta:
        model = models.CompanyImage
        fields = '__all__'
CompanyImageFormset = forms.inlineformset_factory(models.Settings,models.CompanyImage,form = CompanyImageForm,can_delete = True,extra = 1)


class CompanyAdminForm(forms.ModelForm):
    class Meta:
        model = models.CompanyAdmin
        fields = '__all__'
        widgets = {
            'title':forms.Textarea(attrs={
                'rows':1,
                'placeholder':'Administrator title/role'
            })
        }


class CompanyAdminBaseInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            user = form.cleaned_data.get("user")
            title = form.cleaned_data.get("title")

            if user is not None and title is None:
                msg= "You must provide an administrator title if a user has been chosen"
                form.add_error('title',msg)
                raise ValidationError("Invalid form error in Administrators tab")
CompanyAdminFormset = forms.inlineformset_factory(models.Settings,models.CompanyAdmin, form = CompanyAdminForm,formset=CompanyAdminBaseInlineFormset,can_delete=True,extra=1)


class CompanySocialMediaForm(forms.ModelForm):
    class Meta:
        model = models.SocialMedia
        fields = '__all__'
CompanySocialMediaFormset = forms.inlineformset_factory(models.Settings, models.SocialMedia,form=CompanySocialMediaForm,can_delete=True,extra=1)   