from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from asgiref.sync import iscoroutinefunction

from app.apps.history.tasks import create_history
from utils.constants import HEADER_USER_ANONYMOUS

class HistoryMiddleware(MiddlewareMixin):

    def __call__(self, request):
        # Exit out to async mode, if needed
        if iscoroutinefunction(self):
            return self.__acall__(request)
        response = None
        start_time = now()
        if hasattr(self, "process_request"):
            response = self.process_request(request)
        response = response or self.get_response(request)
        end_time = now()
        if hasattr(self, "process_response"):
            response = self.process_response(request, response, end_time, start_time)
        return response

    def process_response(self, request, response, end_time, start_time):
        data_historica = {
            "response_time_second": (end_time - start_time).total_seconds(),
            "datetime_end": str(end_time),
            "datetime_init": str(start_time),
            "response_status_code": 200,
            "user_uuid": None,
            "user": None,
            "check_user": True,
        }

        if hasattr(request, 'method'):
            if request.method in ['OPTIONS', 'HEAD']:
                return response
            data_historica["request_method"] = request.method
        
        if request.META.get("SERVER_NAME"):
            if request.META.get("SERVER_NAME") == 'testserver': #skip when running test
                return response
            data_historica["server_name"] = request.META.get("SERVER_NAME")

        if hasattr(response, 'status_code'):
            data_historica["response_status_code"] = response.status_code

        if hasattr(request, 'user'):
            if not request.user.is_anonymous:
                data_historica["user"] = request.user.pk
            else:
                if HEADER_USER_ANONYMOUS in request.headers:
                    data_historica["user_uuid"] = request.headers.get(HEADER_USER_ANONYMOUS)
                else:
                    data_historica["check_user"] = False

        if hasattr(request, "path"):
            data_historica["path_url"] = request.path

        if request.META.get("HTTP_USER_AGENT"):
            data_historica["http_user_agent"] = request.META.get("HTTP_USER_AGENT")

        if request.META.get("REMOTE_ADDR"):
            data_historica["remote_address"] = request.META.get("REMOTE_ADDR")

        if request.META.get("QUERY_STRING"):
            data_historica["query_string"] = request.META.get("QUERY_STRING")             

        create_history.delay(data_historica)
        return response