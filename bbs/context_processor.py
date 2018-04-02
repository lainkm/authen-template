# from django.conf import settings as original_settings
 
 
def logo(request):
	return {"logo": "Authen"}
 
 
# def ip_address(request):
#     return {'ip_address': request.META['REMOTE_ADDR']}