from django.urls import path
from . import views as blog_views

app_name = "blog"
urlpatterns = [
    path('blog/categories',blog_views.ViewBlogCategories.as_view(),name='view-blog-categories'),
    path('blog/category/add',blog_views.AddBlogCategory.as_view(),name='add-blog-category'),
    path('blog/category/<int:pk>/',blog_views.UpdateBlogCategory.as_view(),name='update-blog-category'),
    path('blog/category/<int:pk>/delete',blog_views.DeleteBlogCategory.as_view(),name='delete-blog-category'),
    path('blog/category/delete',blog_views.DeleteBlogCategory.as_view(),name='delete-blog-categorys'),

    path('blog/articles',blog_views.ViewBlogArticles.as_view(),name='view-blog-articles'),
    path('blog/article/add',blog_views.AddBlogArticle.as_view(),name='add-blog-article'),
    path('blog/article/<int:pk>/',blog_views.UpdateBlogArticle.as_view(),name='update-blog-article'),
    path('blog/article/<int:pk>/delete',blog_views.DeleteBlogArticle.as_view(),name='delete-blog-article'),
    path('blog/article/delete',blog_views.DeleteBlogArticle.as_view(),name='delete-blog-articles'),
]