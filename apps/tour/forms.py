from django import forms 
from django.core.exceptions import ValidationError
from . import models
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext_lazy as _

class FormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        #self.form_class='form-horizontal'
        self.label_class='text-start text-md-end'
        #self.field_class='col'
        self.template = 'tour/bootstrap4/table_inline_formset.html'

class TourDestinationForm(forms.ModelForm):    
    class Meta:
        model = models.TourDestination
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='tour-destination-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'


class TourCategoryForm(forms.ModelForm):   
    class Meta:
        model = models.TourCategory
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='tour-category-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'


class TourForm(forms.ModelForm):    
    class Meta:
        model = models.Tour
        fields = '__all__'
        widgets = {
            'description':forms.Textarea(attrs={'rows':2}),
            'ad_description':forms.Textarea(attrs={'rows':2})
            }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='tour-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'
        self.helper.form_tag = False

    def clean(self):
        self.cleaned_data = super(TourForm,self).clean()
        #advertise = self.cleaned_data["advertise"]
        #ad_title = self.cleaned_data["ad_title"]
        #ad_name = self.cleaned_data["ad_name"]
        #ad_description = self.cleaned_data["ad_description"]

        if self.cleaned_data["advertise"] is True and self.cleaned_data["ad_title"] is None and self.cleaned_data["ad_name"] is None:
            title_msg = "You must provide an ad title if advertise is checked"
            name_msg = "You must provide an ad name if advertise is checked"
            desc_msg = "You must provide an ad description if advertise is checked"
            self.add_error('ad_title',title_msg)
            self.add_error('ad_name',name_msg)
            self.add_error('ad_description',desc_msg)
            raise ValidationError("Invalid form error(s) in general tab")
        elif self.cleaned_data["advertise"] is False and self.cleaned_data["ad_title"] is not None and self.cleaned_data["ad_name"] is not None:
            self.cleaned_data["ad_title"] = ""
            self.cleaned_data["ad_name"] = ""
            self.cleaned_data["ad_description"] = ""
        return self.cleaned_data


class TourBookingForm(forms.ModelForm):    
    class Meta:
        model = models.TourBooking
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='booking-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'


class TourReviewForm(forms.ModelForm):
    class Meta:
        model = models.TourReview
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='tour-review-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'

    def clean(self):
        super().clean() 
        super().non_field_errors()
        rating = self.cleaned_data.get("rating")
        if rating is not None and rating > 5.0:
            msg = "The maximum rating value is 5.0"
            self.add_error('rating',msg)
            raise ValidationError("Invalid form error, please check form and ensure all fields are valid")
            

class TourImageForm(forms.ModelForm):
    class Meta:
        model = models.TourImage
        fields = '__all__'
TourImageFormset = forms.inlineformset_factory(models.Tour, models.TourImage,fields='__all__',extra=1)


class TourInclusionForm(forms.ModelForm):
    class Meta:
        model = models.TourInclusion
        fields = '__all__'
        widgets = { 'description':forms.Textarea(attrs={'rows':2})}
TourInclusionFormset = forms.inlineformset_factory(models.Tour,models.TourInclusion,fields='__all__',form = TourInclusionForm,extra=1)


class TourInsightForm(forms.ModelForm):
    class Meta:
        model = models.TourInclusion
        fields = '__all__'
        widgets = { 'description':forms.Textarea(attrs={'rows':2})}
TourInsightsFormset = forms.inlineformset_factory(models.Tour,models.TourInsight,fields='__all__',form = TourInsightForm,extra=1)


class TourQuestionForm(forms.ModelForm):
    class Meta:
        model = models.TourQuestion
        fields = '__all__'
TourQuestionsFormset = forms.inlineformset_factory(models.Tour,models.TourQuestion,fields='__all__',extra=1)


class RelatedTourForm(forms.ModelForm):
    class Meta:
        model = models.RelatedTour
        fields = '__all__'
RelatedTourFormset = forms.inlineformset_factory(models.Tour,models.RelatedTour,fk_name="tour", fields='__all__',extra=1)


class TourTagForm(forms.ModelForm):
    class Meta:
        model = models.TourTag
        fields = '__all__'
TourTagFormset = forms.inlineformset_factory(models.Tour,models.TourTag,fields='__all__',extra=1)


class TourProgramForm(forms.ModelForm):
    class Meta:
        model = models.TourProgram
        fields = '__all__'
        widgets = { 'description':forms.Textarea(attrs={'rows':2})}
TourProgramFormset = forms.inlineformset_factory(models.Tour,models.TourProgram,fields='__all__',form = TourProgramForm,extra=1)