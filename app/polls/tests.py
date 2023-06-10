import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self,):
        """was_published_recently() returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day"""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self,):
        """was_published_recently() returns True for questions whose pub_date
        is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """ Create a question with the given `question_text`
    and published the given number of `days offset to now (negative fro questions published in the past, positive for questions that have yet to be published)`"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        

    def test_past_question(self,):
        """Questions with a pub_date in the past are displayed on the index page."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self,):
        """Questions with a pub_date in the future aren't displayed on  the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")

        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Pass question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """The detail view of a question with a pub_date in the future 
        return a 404 not found"""
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        display the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from polls import apiviews

class TestPolls(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = apiviews.QuestionViewSet.as_view({'get': 'list'})
        self.uri = '/polls/polls/'

        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        #self.token.save()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test1234'
        )

    def test_list(self):
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION='Token {0}'.format(self.token.key))
        #request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 
                        'Expected Response Code 200, received {0} instead'.format(response.status_code))
        
    def test_list2(self):
        self.client.login(username='test', password="test1234")
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200, 
                         'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    def test_create(self):
        self.client.login(username='test', password="test1234")
        params = {
            "question_text": "my question",
            "pub_date": "2023-01-02", 
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201, 
                         'Expected response code 201, received {0} instead'.format(response.status_code))

