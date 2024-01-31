from django.db import models
from django.contrib.auth import get_user_model


class History(models.Model):
    path_url = models.CharField(max_length=512, )
    server_name = models.CharField(max_length=512)
    query_string = models.TextField(null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    user_uuid = models.CharField(max_length=255, null=True)
    check_user = models.BooleanField(default=True) #user with id or uuid
    datetime_init = models.DateTimeField()
    http_user_agent = models.CharField(max_length=512, null=True)
    remote_address = models.GenericIPAddressField()

    request_method = models.CharField(max_length=100)
    response_status_code = models.PositiveSmallIntegerField(default=200)
    response_time_second = models.DecimalField(max_digits=10, decimal_places=6)
    datetime_end = models.DateTimeField()

