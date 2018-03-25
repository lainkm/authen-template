from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from bbs import settings
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
	# BIRTH_YEAR_CHOICES = ('1980', '1981', '1982','1983','1984')
	nickname = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		max_length=30, label='NickName', required=False)
	# url = forms.CharField(
	# 	widget=forms.TextInput(attrs={'class': 'form-control'}),
	# 	max_length=50, label='Url', required=False)
	location = forms.CharField(
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		max_length=50, label='Location', required=False)

	# sex = forms.ChoiceField(choices=[('male', 'male'), ('female', 'female')],
	# 	widget=forms.RadioSelect(attrs={'class': 'form-control'}),
	# 	label='Sex',
	# ) 
	# birthday = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
	# resume = forms.CharField(
	# 		widget=forms.TextInput(attrs={'class': 'form-control'}),
	# 		max_length=300, label='Resume', required=False)

	class Meta:
		model = UserProfile
		fields = ['nickname', 'location']

def forbidden_username_validator(value):
	"""
	被禁用的用户名，注册时会报错
	"""
	forbidden_usernames = {
		'admin', 'settings', 'news', 'about', 'help', 'signin', 'signup',
		'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout',
		'administrator', 'join', 'account', 'username', 'root', 'blog',
		'user', 'users', 'billing', 'subscribe', 'reviews', 'review', 'blog',
		'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs', 'contribute',
		'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
		'campaign', 'config', 'delete', 'remove', 'forum', 'forums',
		'download', 'downloads', 'contact', 'blogs', 'feed', 'feeds', 'faq',
		'intranet', 'log', 'registration', 'search', 'explore', 'rss',
		'support', 'status', 'static', 'media', 'setting', 'css', 'js',
		'follow', 'activity', 'questions', 'articles', 'network', }
	if value.lower() in forbidden_usernames:
		raise ValidationError('This is a reserved word.')

def invalid_username_validator(value):
	"""
	无效的用户名，用户名不能出现'@', '+', '-'
	"""
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('Enter a valid username.')

def unique_email_validator(value):
	"""
	保证邮箱唯一
	"""
	if UserProfile.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this Email already exists.')

def unique_username_ignore_case_validator(value):
	"""
	username忽略大小写验证唯一
	"""
	if UserProfile.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this Username already exists.')

def signup_domain_validator(value):
	"""
	允许注册的邮箱域名
	"""
	if '*' in settings.ALLOWED_SIGNUP_DOMAINS:
		return

	domain = value[value.index("@"):]

	if domain not in settings.ALLOWED_SIGNUP_DOMAINS:
		allowed_domain = ','.join(settings.ALLOWED_SIGNUP_DOMAINS)
		msg = _('Invalid domain. '
			'Allowed domains on this network: {0}').format(allowed_domain)
		raise ValidationError(msg)


class RegisterForm(forms.ModelForm):
	"""
	username, email唯一，使用email或username登陆
	"""
	username = forms.CharField(label="Username",
		widget=forms.TextInput(attrs={'class': 'form-control'}),
		help_text='Username can\'t changed once create.',
		max_length=30)
	email = forms.CharField(label="Email",
		widget=forms.EmailInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label="Password",
		widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	confirm_password = forms.CharField(label="Confirm Password",
		widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = UserProfile
		exclude = ['last_login', 'date_joined']
		fields = ['username', 'email', 'password', 'confirm_password', ]

	def __init__(self, *args, **kwargs):
		"""
		验证用户名和邮箱的有效性
		"""
		super(RegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators += [
			forbidden_username_validator, 
			invalid_username_validator,
			unique_username_ignore_case_validator,
		]
		self.fields['email'].validators += [
			unique_email_validator, 
			signup_domain_validator,
		]

	def clean(self):
		"""
		验证密码一致，一定要返回cleaned_date
		"""
		super(RegisterForm, self).clean()
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password and password != confirm_password:
			self._errors['password'] = self.error_class(
				['Passwords don\'t match'])
		return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	"""
	重置密码表单类
	"""
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		label="Old password", required=True)
	new_password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		label="New password", required=True)
	confirm_password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		label="Confirm new password", required=True)

	class Meta:
		model = UserProfile
		fields = ['id', 'old_password', 'new_password', 'confirm_password']

	def clean(self):
		super(ChangePasswordForm, self).clean()

		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')

		user_id = self.cleaned_data.get('id')
		user = UserProfile.objects.get(pk=user_id)

		if not user.check_password(old_password):
			self._errors['old_password'] = self.error_class(
				['Old password don\'t match'])

		if new_password and new_password != confirm_password:
			self._errors['new_password'] = self.error_class(
				['Passwords don\'t match'])

		if new_password == old_password:
			self._errors['new_password'] = self.error_class(
				['Passwords don\'t change'])

		return self.cleaned_data

class SavePictureForm(forms.Form):
    x = forms.IntegerField(min_value=0)
    y = forms.IntegerField(min_value=0)
    width = forms.IntegerField(min_value=0)
    height = forms.IntegerField(min_value=0)
