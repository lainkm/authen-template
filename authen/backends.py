# from django.contrib.auth.models import User
# from django.contrib.auth.backends import ModelBackend

# class EmailAuthModelBackend(ModelBackend):
# 	def authenticate(self, username=None, password = None, is_staff = None):
# 		try:
# 			user = User.objects.get(email=username)
# 			if user.check_password(password):
# 				if is_staff is not None:
# 					if user.is_staff == is_staff:
# 						return user
# 				else:
# 					return None
# 				return user

# 		except User.DoesNotExist:
# 			return None


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile

# 让用户可以用邮箱或者用户名登录
# setting 里要有对应的配置
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(email=username) | Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None