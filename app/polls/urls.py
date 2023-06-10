from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .apiviews import QuestionViewSet, ChoiceList, UserCreate, LoginView



from rest_framework.documentation import include_docs_urls


app_name="polls"

router = DefaultRouter()
router.register('polls', QuestionViewSet, basename='polls')

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"), 

    #apis
    path("choices/", ChoiceList.as_view(), name="choce_list"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),

    path(r'docs/', include_docs_urls(title='Polls API'))
]

urlpatterns +=router.urls