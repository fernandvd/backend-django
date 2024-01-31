from rest_framework.routers import DefaultRouter

from .views import HistoryReadOnlyModelViewset

app_name = "history"

route = DefaultRouter()
route.register("history", HistoryReadOnlyModelViewset)

urlpatterns = []

urlpatterns += route.urls
