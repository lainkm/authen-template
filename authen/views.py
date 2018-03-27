from django.shortcuts import render, redirect, get_object_or_404

# from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login

from .forms import RegisterForm, ProfileForm, ChangePasswordForm, SavePictureForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.views.generic import ListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import cloudinary.uploader
from bbs.base_settings import CLOUD_NAME, CLOUD_KEY, CLOUD_SECRET

# 先注册
cloudinary.config( 
  cloud_name = CLOUD_NAME, 
  api_key = CLOUD_KEY, 
  api_secret = CLOUD_SECRET)

def register(request):
    """
    注册界面
    使用唯一的username和password创建用户(django2.0)
    使用唯一的username,email和password创建用户(django1.9之前)
    """
    if request.method != 'POST':
        form = RegisterForm()
        return render(request, 'authen/register.html', {'form': form})

    form = RegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'authen/register.html', {'form': form})

    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    # UserProfile.objects.create_user(username=username, password=password), 可以但是我们也想保存email数据
    
    email = form.cleaned_data.get('email')
    UserProfile.objects.create_user(username=username, password=password, email=email)

    # 创建完直接冲定向到首页
    user = authenticate(username=username, password=password)
    login(request, user)

    return redirect('/')

# def index(request):
#     print('hah')
#     users_list = UserProfile.objects.all()
#     print(users_list)
#     return render(request, 'authen/index.html', {'users_list':'users_list'})

class IndexView(ListView):
    """
    首页，返回用户的别名和他们的个人描述
    """
    model = UserProfile
    template_name = 'authen/index.html'
    context_object_name = 'user_list'
    paginate_by = 6


def profile(request, username):
    """
    个人主页，返回个人信息，自己和其他用户都能看到，自己可编辑
    """
    page_user = get_object_or_404(UserProfile, username=username)

    context = {
        'page_user': page_user
    }
    return render(request, 'authen/profile.html', context)

@login_required
def settings(request):
    """
    用户编辑自己的个人信息
    """
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.nickname = form.cleaned_data.get('nickname')
            # user.profile.resume = form.cleaned_data.get('resume')
            # user.profile.url = form.cleaned_data.get('url')
            user.location = form.cleaned_data.get('location')
            # user.profile.sex = form.cleaned_data.get('sex')
            user.save()

            message = 'Your profile were successfully edited.'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect(f'/auth/{user.username}/')

    else:
        initial = {
            'nickname': user.nickname,
            # 'birthday': user.birthday,
            # 'url': user.profile.url,
            'location': user.location,
            # 'resume': user.profile.resume,
            # 'sex': user.profile.sex,
        }
        form = ProfileForm(instance=user, initial=initial)

    return render(request, 'authen/settings.html', {'form': form})

@login_required
def password(request):
    user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()

            message = 'Your password were successfully changed. Please relogin'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('/auth/login/')
        # else:
        #     return render(request, 'authen/password.html', {'form': form})

    else:
        form = ChangePasswordForm(instance=user)
    
    return render(request, 'authen/password.html', {'form': form})



@login_required
def picture(request):
    uploaded_picture = False
    picture_url = None
    username = request.user.username
    print(request.GET)
    if request.GET.get('upload_picture') == 'uploaded':
        print('waiting..')
        uploaded_picture = True
        result = cloudinary.uploader.explicit(username, type='upload')
        picture_url = result['secure_url']
        print(picture_url)

    context = {
        'uploaded_picture': uploaded_picture,
        'picture_url': picture_url,
    }
    return render(request, 'authen/picture.html', context)


@login_required
def upload_picture(request):
    # return render(request, 'authen/register.html')
    username = request.user.username

    cloudinary.uploader.upload(request.FILES['picture'],
                               public_id=username, width=400, crop='limit')

    return redirect('/auth/picture/?upload_picture=uploaded')

@login_required
def save_uploaded_picture(request):
    form = SavePictureForm(request.POST)
    user = request.user

    if form.is_valid():
        form.cleaned_data.update(crop='crop')
        result = cloudinary.uploader.explicit(
            user.username, type='upload', eager=form.cleaned_data)

        # https://cloudinary.com/console/media_library/asset/image/upload/2
        user.picture_url = result['eager'][0]['secure_url']
        user.save()

    return redirect(f'/auth/{user.username}/')
