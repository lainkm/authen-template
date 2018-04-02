
import sys
from django.views.debug import technical_500_response
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class UserBasedExceptionMiddleware(MiddlewareMixin):
	def process_exception(self, request, exception):
		print(request.META.get('REMOTE_ADDR'))
		# if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
		if repr(request.META.get('REMOTE_ADDR')) == repr("127.0.0.1"):  # 允许的ip
			print("ahah")
			return technical_500_response(request, *sys.exc_info())
