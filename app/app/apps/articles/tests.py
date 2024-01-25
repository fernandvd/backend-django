from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Comment, Article, Tag


class ArticleAPiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='test',
            password='password',
        )
        self.article = Article.objects.create(
            slug = "slug",
            title = "titulo",
            description = "descripcion",
            body = "body ",
            author = self.user.profile,
        )

        self.url_name_article = 'articles:article-list'
        self.url_name_article_detail = 'articles:article-detail'
        self.url_name_article_feed = 'articles:article-feed'
        self.url_name_article_favorite = 'articles:article-favorite'
        self.url_name_article_comment = 'articles:article-comments'
        self.url_name_article_comment_delete = 'articles:article-comment-delete'
        self.url_name_tags = 'articles:tag-list'

    def test_list_article(self):
        url = reverse(self.url_name_article)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIn('articles', response_json)
        self.assertIn('articlesCount',response_json)

    def test_create_article(self):
        data = {
            "article": {
                "description": "description",
                "body": "body",
                "title": "title random",
                "tagList": ["tag1", "tag2"]
            }
        }
        url = reverse(self.url_name_article)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('slug', response.data)

    def test_retrieve_article(self):
        url = reverse(self.url_name_article_detail, kwargs={'slug': self.article.slug})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('body', response.data)
        self.assertIn('slug', response.data)

    def test_retrieve_article_non_exist(self):
        url = reverse(self.url_name_article_detail, kwargs={'slug': "slug-not-exist"})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article(self):
        new_body = "body Changed"
        url = reverse(self.url_name_article_detail, kwargs={'slug': self.article.slug})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data = {"article": {"body": new_body}}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('body', response.data)
        self.assertEqual(new_body, response.data.get("body"))

    def test_article_feed(self):
        url = reverse(self.url_name_article_feed)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIn('articles', response_json)
        self.assertIn('articlesCount', response_json)

    def test_article_favorite(self):
        self.article.refresh_from_db()
        url = reverse(self.url_name_article_favorite, kwargs={"article_slug": self.article.slug})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('slug', response.data)
        self.assertEqual(self.article.slug, response.data.get('slug'))

    def test_article_unfavorite(self):
        self.article.refresh_from_db()
        url = reverse(self.url_name_article_favorite, kwargs={"article_slug": self.article.slug})
        self.client.force_authenticate(user=self.user)
        self.client.post(url, {}, format='json')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user.profile.has_favorited(self.article))

    def test_article_comments_list(self):
        url = reverse(self.url_name_article_comment, kwargs={'article_slug': self.article.slug})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertIn('comments', response_json)
        self.assertIn('commentsCount', response_json)

    def test_article_comments_create(self):
        comment_body = "comentario"
        data = {
            "comment": {
                "body": comment_body
            }
        }
        url = reverse(self.url_name_article_comment, kwargs={'article_slug': self.article.slug})

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url,data,format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('body', response.data)
        self.assertEqual(comment_body, response.data.get('body'))

    def test_article_comments_destroy(self):
        comment_body = "comentario"
        comment = Comment.objects.create(
            body =comment_body,
            article =self.article,
            author =self.user.profile,
        )
        url = reverse(self.url_name_article_comment_delete, kwargs={'article_slug': self.article.slug, "comment_pk": comment.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_tag_list(self):
        num_tags = 3
        for i in range(num_tags):
            Tag.objects.create(tag=f"tag{i}", slug=f"slug{i}")
        url = reverse(self.url_name_tags)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tags', response.data)
        self.assertEqual(len(response.data.get('tags')), num_tags)
