from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import	reverse

# class Profile(models.Model):
#   """
#     使用增加一对一外键的方法，添加其他user属性
#   """
# 	user = models.OneToOneField(User,on_delete=models.CASCADE)
# 	nickname = models.CharField(max_length=50, null=True, blank=True)
# 	location = models.CharField(max_length=50, null=True, blank=True)
# 	url = models.CharField(max_length=50, null=True, blank=True)
# 	picture_url = models.CharField(max_length=150, null=True, blank=True)
# 	sex = models.CharField(max_length=50, default='male', choices=(('male','male'), ('female', 'female')))
# 	resume = models.CharField(max_length=300, null=True, blank=True)
# 	# birthday = models.DateTimeField()

# 	def get_url(self):
# 		url = self.url
# 		if not self.url.startwith('http://') \
# 			and not self.url.startwith('https://') \
# 			and len(self.url) > 0:
# 			url = "http://" + str(self.url)
# 		return url

# 	def get_picture(self):
# 		if not self.picture_url:
# 			picture = '/static/img/favicon.ico'
# 		picture = self.picture_url
# 		return picture


class UserProfile(AbstractUser):
	"""
	使用重写User的方法，添加user详细信息
	"""
	nickname = models.CharField(max_length=50, verbose_name='昵称', default='')
	birthday = models.DateField(null=True, blank=True, verbose_name='生日')
	gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='female', verbose_name='性别')
	address = models.CharField(max_length=100, default='', verbose_name='地址')
	mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
	image = models.ImageField(max_length=100, upload_to='image/%Y/%m', default='image?default.png', verbose_name='头像')
	picture_url = models.CharField(max_length=120, null=True, blank=True)
	resume = models.CharField(max_length=300, null=True, blank=True, verbose_name='简介')
	# say = models.CharField(max_length=300, null=True, blank=True, verbose_name='昵称')
	location = models.CharField(max_length=50, null=True, blank=True)

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = verbose_name
		ordering = ['-date_joined']

	def __str__(self):
		return self.username

	def get_picture(self):
		print(self.username, self.picture_url)


		if not self.picture_url:
			no_picture = 'http://res.cloudinary.com/lainly/image/upload/v1521955639/2.png'
			return no_picture

		return self.picture_url

	def get_absolute_url(self):
		"""
			in html ,using 
				<a href="{{ u.get_absolute_url }}">{{ u.username }}</a>
			to replace:
				<a href="{% url 'profile' u.username %}">{{ u.username }}</a>
		"""
		return reverse('profile', kwargs={'username': self.username})



	# def save(self, *args, **kwargs):
		"""
		重写保存到数据库的操作
		"""
		# if not self.summry:
		# md = markdown.Markdown(extensions=[
		# 'markdown.extensions.extra',
		# 'markdown.extensions.codehilite',
		# ])
		# self.summry = strip_tags(md.convert(self.body))[:200]
		# super(Article, self).save(*args, **kwargs)
		#                                               