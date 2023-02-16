from django.db import models
from datetime import datetime, date
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


# BLOG CATEGORY MODEL
class BlogCategory(models.Model):
    STATUS = (
        (True, "Enabled"),
        (False, "Disabled")
    )
    blog_category_slug = models.SlugField(
        max_length=255, unique=True, editable=False, null=True)
    name = models.CharField("category", max_length=60, unique=True)
    image = models.ImageField(
        default="system/default.png", upload_to='blog/categories')
    description = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(choices=STATUS, default=1)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def save(self, *args, **kwargs):
        self.blog_category_slug = slugify(self.name)
        super(BlogCategory, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            newimg = (500, 500)
            img.thumbnail(newimg)
            img.save(self.image.path)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:update-blog-category", kwargs={"pk": self.pk})


# BLOG ARTICLE MODEL
class BlogArticle(models.Model):
    STATUS = (
        (True, "Enabled"),
        (False, "Disabled")
    )
    article_slug = models.SlugField(
        max_length=255, unique=True, editable=False, null=True, blank=True)
    article_title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        default="system/default.png", upload_to='blog/articles')
    category = models.ForeignKey(
        BlogCategory, related_name="blog_articles", on_delete=models.PROTECT)
    article_intro = models.TextField(
        "Introduction", max_length=900, help_text="The article Intro can be up to a maximum of 900 words")
    article = models.TextField()
    publish_date = models.DateField(auto_now=True, editable=False)
    status = models.BooleanField(choices=STATUS, default=1)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('artcles')

    def save(self, *args, **kwargs):
        # if not self.id:
        self.article_slug = slugify(self.article_title)
        super(BlogArticle, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        newimg = (5000, 400)
        img.thumbnail(newimg)
        img.save(self.image.path)

    def __str__(self):
        return f'article title is ${self.article_title}'

    def get_absolute_url(self):
        return reverse("blog:update-blog-article", kwargs={"pk": self.pk})