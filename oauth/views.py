from django.shortcuts import render
from django.conf import settings
import urllib.request, urllib.parse, urllib.error
from django.http import HttpResponseRedirect  
import json
from authen.models import UserProfile
from django.contrib.auth import authenticate,login
from django.urls import reverse

GITHUB_CLIENTID = settings.GITHUB_CLIENTID
GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
GITHUB_CALLBACK = settings.GITHUB_CALLBACK
GITHUB_AUTHORIZE_URL = settings.GITHUB_AUTHORIZE_URL

# 这里不是很明白
def _get_refer_url(request):
    refer_url = request.META.get('HTTP_REFER', 
    '/')
    # print(request.META)
    print('REFER', refer_url)
    host = request.META['HTTP_HOST']
    # print(host)
    if refer_url.startswith('http') and host not in refer_url:
        refer_url = '/'
    return refer_url

# 第一步: 请求github第三方登录
def githhub_login(request):
    """
    github.com/login/oauth/authorize?client_id=75b9c0ef635dab41fe00&client_secret=b4b6062336049bbd73dc1b4c32e91afad642e086&redirect_uri=http%3A%2F%2Flocalhost%3A8001%2Foauth%2Fgithub%2F&state=%2Findex%28自己的首页%29
    """
    data = {
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'redirect_uri': GITHUB_CALLBACK,
        'state': _get_refer_url(request),
    }
    # print(_get_refer_url(request))
    github_auth_url = '%s?%s' % \
    (GITHUB_AUTHORIZE_URL,urllib.parse.urlencode(data))
    print('git_hub_auth_url',github_auth_url)
    return HttpResponseRedirect(github_auth_url)

# github认证处理
def github_auth(request):
    template_html = 'authen/index.html'

    # 如果申请登陆页面成功后，就会返回code和state(被坑了好久)
    if 'code' not in request.GET:
        return render(request,template_html)

    code = request.GET.get('code')
    print("code: ", code)

    # 第二步
    # 将得到的code，通过下面的url请求得到access_token
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'code': code,
        'redirect_uri': GITHUB_CALLBACK,
    }

    # json对象生成url格式
    data = urllib.parse.urlencode(data)
    print('DATA',data)

    # 请求参数需要bytes类型
    binary_data = data.encode('utf-8')
    print('data:', data)

    # 设置请求返回的数据类型
    headers={'Accept': 'application/json'}
    req = urllib.request.Request(url, binary_data, headers)
    print('req:', req)
    response = urllib.request.urlopen(req) 
    print('response', response)

    result = response.read()
    print(result)

    # json是str类型的，将bytes转成str
    result = result.decode('ascii')
    result = json.loads(result)
    access_token = result['access_token']
    print('access_token:', access_token)

    # 将token发送给资源服务器获得数据
    url = 'https://api.github.com/user?access_token=%s' \
     % (access_token)
    response = urllib.request.urlopen(url) # 不用参数，所以不用request对象也行
    html = response.read()
    html = html.decode('ascii')
    data = json.loads(html)
    print(data)
    username = data['login']
    print('username:', username)
    password = '111111'
    picture_url = data['avatar_url']



    # 如果不存在username，则创建
    try:
        user1 = UserProfile.objects.get(username=username)
        print('user1')
    except:
        user2 = UserProfile.objects.create_user(username=username, 
        password=password)
        user2.picture_url = picture_url
        print('user2', user2.picture_url)
        user2.save()
        # profile = Profile.objects.create(user=user2)
        # profile.save()

    # 登陆认证
    user = authenticate(username=username, 
    password=password)
    login(request, user)
    return HttpResponseRedirect(reverse('index'))
# from django.shortcuts import render
# from django.conf import settings
# import urllib.request, urllib.parse, urllib.error
# from django.http import HttpResponseRedirect  

# GITHUB_CLIENTID = settings.GITHUB_CLIENTID
# GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
# GITHUB_CALLBACK = settings.GITHUB_CALLBACK
# GITHUB_AUTHORIZE_URL = settings.GITHUB_AUTHORIZE_URL

# def _get_refer_url(request):
#     refer_url = request.META.get('HTTP_REFER', 
#     '/index(自己的首页)')
#     host = request.META['HTTP_HOST']
#     if refer_url.startswith('http') and host not in refer_url:
#         refer_url = '/index'
#     return refer_url

# # 第一步: 请求github第三方登录
# def githhub_login(request):
#     data = {
#         'client_id': GITHUB_CLIENTID,
#         'client_secret': GITHUB_CLIENTSECRET,
#         'redirect_uri': GITHUB_CALLBACK,
#         'state': _get_refer_url(request),
#     }
#     github_auth_url = '%s?%s' % \
#     (GITHUB_AUTHORIZE_URL,urllib.parse.urlencode(data))
#     print(('git_hub_auth_url',github_auth_url))
#     return HttpResponseRedirect(github_auth_url)

# # github认证处理
# def github_auth(request):
#     template_html = 'authen/login.html'

#     # 如果申请登陆页面成功后，就会返回code和state(被坑了好久)
#     if 'code' not in request.GET:
#         return render(request,template_html)

#     code = request.GET.get('code')

#     # 第二步
#     # 将得到的code，通过下面的url请求得到access_token
#     url = 'https://github.com/login/oauth/access_token'
#     data = {
#         'grant_type': 'authorization_code',
#         'client_id': GITHUB_CLIENTID,
#         'client_secret': GITHUB_CLIENTSECRET,
#         'code': code,
#         'redirect_uri': GITHUB_CALLBACK,
#     }

#     data = urllib.parse.urlencode(data)

#     # 请求参数需要bytes类型
#     binary_data = data.encode('utf-8')
#     print(('data:', data))

#     # 设置请求返回的数据类型
#     headers={'Accept': 'application/json'}
#     req = urllib.request.Request(url, binary_data,headers)
#     print(('req:', req))
#     response = urllib.request.urlopen(req) 

#     # json是str类型的，将bytes转成str
#     result = result.decode('ascii')
#     result = json.loads(result)
#     access_token = result['access_token']
#     # print('access_token:', access_token)

#     url = 'https://api.github.com/user?access_token=%s' \
#      % (access_token)
#     response = urllib.request.urlopen(url)
#     html = response.read()
#     html = html.decode('ascii')
#     data = json.loads(html)
#     username = data['name']
#     # print('username:', username)
#     password = '111111'

#     # 如果不存在username，则创建
#     try:
#         user1 = User.objects.get(username=username)
#     except:
#         user2 = User.objects.create_user(username=username, 
#         password=password)
#         user2.save()
#         profile = Profile.objects.create(user=user2)
#         profile.save()

#     # 登陆认证
#     user = authenticate(username=username, 
#     password=password)
#     login(request, user)
#     return HttpResponseRedirect(reverse('index'))