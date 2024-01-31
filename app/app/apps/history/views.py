from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import ListHistorySerializer
from .models import History


class HistoryReadOnlyModelViewset(ReadOnlyModelViewSet):
    queryset = History.objects.select_related('user')
    serializer_class = ListHistorySerializer

    filterset_fields = {
        'check_user': ['exact'],
        'path_url': ['exact', 'icontains'],
        'request_method': ['exact',],
        'response_status_code': ['exact',],
        'user_id': ['exact',],
    }
