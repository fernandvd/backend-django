from celery import shared_task

from .serializers import CreateHistorySerializer

@shared_task
def create_history(data):
    serializer = CreateHistorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
