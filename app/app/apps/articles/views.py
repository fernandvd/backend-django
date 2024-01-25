from rest_framework import generics, mixins, status, viewsets 
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Comment, Tag
from .renderers import ArticleJSONRenderer, CommentJSONRenderer
from .serializers import ArticleSerializer, CommentSerializer, TagSerializer

class ArticleViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer, )
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = self.queryset

        author = self.request.query_params.get('author')
        if author is not None and author!='':
            queryset = queryset.filter(author_user_username=author)

        tag = self.request.query_params.get('tag',)
        if tag is not None and tag!='':
            queryset = queryset.filter(tags__tag=tag)

        favorited_by = self.request.query_params.get('favorited')
        if favorited_by is not None and favorited_by!='':
            queryset = queryset.filter(
                favorited_by__user__username=favorited_by
            )

        return queryset
    
    def get_serializer_context(self):
        if self.request.user.is_anonymous:
            return super().get_serializer_context()
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'author': self.request.user.profile
        }
    
    def create(self, request, *args, **kwargs):
        serializer_data = request.data.get('article', {})

        serializer = self.get_serializer(
            data=serializer_data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        
        serializer_data = request.data.get('article', {})

        serializer = self.get_serializer(
            serializer_instance,
            data=serializer_data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'article__slug'
    lookup_url_kwarg = 'article_slug'

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.select_related(
        'article', 'article__author', 'article__author__user',
        'author', 'author__user',
    )

    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return queryset.filter(**filters)
    
    def create(self, request, article_slug=None):
        data = request.data.get('comment', {})
        context = {'author': request.user.profile}

        try:
            context['article'] = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CommentsDestroyAPIView(generics.DestroyAPIView):
    lookup_url_kwarg = 'comment_pk'
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    
class ArticleFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def delete(self, request, article_slug=None):
        profile = request.user.profile
        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found')
        
        profile.unfavorite(article)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, article_slug=None):
        profile = self.request.user.profile

        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=article_slug)
        except  Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')
        
        profile.favorite(article)

        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny, )
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'tags': serializer.data,
        })
    

class ArticlesFeedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            author__in=self.request.user.profile.follows.all()
        )
