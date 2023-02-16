from django.db.models import fields
from django import forms
from . import models
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext_lazy as _

class BlogCategoryForm(forms.ModelForm):    
    class Meta:
        model = models.BlogCategory
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='blog-category-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'


class BlogArticleForm(forms.ModelForm):    
    class Meta:
        model = models.BlogArticle
        fields = '__all__'
        widgets = {
            'article_intro':forms.Textarea(attrs={'rows':2}),
            'article':forms.Textarea(attrs={'rows':3})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id='blog-article-form'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-12 col-md-3 text-start text-md-end'
        self.helper.field_class='col-12 col-md-9'