from app.apps.core.renderers import CustomJSONRender

class ArticleJSONRenderer(CustomJSONRender):
    object_label = 'article'
    pagination_object_label = 'articles'
    pagination_count_label = 'articlesCount'


class CommentJSONRenderer(CustomJSONRender):
    object_label = 'comment'
    pagination_object_label = 'comments'
    pagination_count_label = 'commentsCount'
