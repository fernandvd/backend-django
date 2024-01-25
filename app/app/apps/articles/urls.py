from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet, ArticleFavoriteAPIView, ArticlesFeedAPIView,
    CommentsListCreateAPIView, CommentsDestroyAPIView, 
    TagListAPIView,
)

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

app_name = 'articles'

urlpatterns = [
    re_path(r'^articles/feed/?$', ArticlesFeedAPIView.as_view(), name='article-feed'),
    re_path(r'^', include(router.urls)),
    re_path(r'^articles/(?P<article_slug>[-\w]+)/favorite/?$', ArticleFavoriteAPIView.as_view(), name='article-favorite'),
    re_path(r'^articles/(?P<article_slug>[-\w]+)/comments/?$', CommentsListCreateAPIView.as_view(), name='article-comments'),
    re_path(r'^articles/(?P<article_slug>[-\w]+)/comments/(?P<comment_pk>[\d]+)/?$', CommentsDestroyAPIView.as_view(), name='article-comment-delete'),
    re_path(r'^tags/?$', TagListAPIView.as_view(), name='tag-list'),
]
