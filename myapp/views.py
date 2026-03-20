from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from myapp import models
from django.contrib import messages
from myapp.models import Userinfo
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
# 总界面
def mcy(request):
    return render(request, '首页页面.html')
# 用户登入
def user_log_in(request):
    # 检查用户是否已经登录
    if 'id' in request.session:
        return redirect(reverse('主页面'))  # 如果已登录，直接跳转到主页面

    if request.method == "GET":
        return render(request, '用户登入界面.html')  # 是否get请求
    elif request.method == "POST":
        Account = request.POST.get("Account")
        password = request.POST.get("password")
        print(f"账号和密码为:{Account, password}")
        try:
            if Account == models.Userinfo.objects.filter(Account=Account).first().Account and password == models.Userinfo.objects.filter(
                    Account=Account).first().password :
                request.session['id'] = models.Userinfo.objects.filter(Account=Account).first().id
                # return HttpResponse("登入成功")
                return redirect(reverse('主页面'))
            else:
                error_msg = "用户名或密码错误"
                return render(request, '用户登入界面.html', {'error_msg': error_msg})
        except Exception as e:
                error_msg = "用户名或密码错误"
                return render(request, '用户登入界面.html', {'error_msg': error_msg})

    # return render(request, '用户登入界面.html')
# 用户注册
def user_register(request):
    if request.method == 'GET':
        return render(request,"用户注册.html")
    if request.method == 'POST':
        name = request.POST.get("username")
        Account = request.POST.get("Account")
        email = request.POST.get("email")
        password = request.POST.get("password")
        age = request.POST.get("age")
        gender = request.POST.get("sex")
        # 验证表单数据
        errors = []

        # 检查必填字段
        if not name:
            errors.append('用户名不能为空')
        if not password:
            errors.append('密码不能为空')

        # 检查用户名是否已存在
        if Userinfo.objects.filter(name=name).exists():
            errors.append('用户名已存在，请选择其他用户名')

        # 检查邮箱是否已存在（如果提供了邮箱）
        if email and Userinfo.objects.filter(email=email).exists():
            errors.append('该邮箱已被注册')

        # 检查密码确认
        if password != password:
            errors.append('两次输入的密码不一致')

        # 检查密码长度
        if password and len(password) < 6:
            errors.append('密码长度至少为6位')

        # 如果没有错误，创建用户
        if not errors:
            try:
                # 创建用户
                models.Userinfo.objects.create(name=name,Account=Account,password=password,age=age,email=email,gender=gender)
                # 显示成功消息
                messages.success(request, f'注册成功！欢迎，{name}！')
                # 重定向到首页
                return redirect('/')

            except Exception as e:
                errors.append(f'注册失败：{str(e)}')
        # 如果有错误，显示错误消息
        for error in errors:
            messages.error(request, error)

    return render(request, '用户注册.html')
#主页面
def main(request):
    nid = request.session.get('id')

    if id:
        try:
            user = models.Userinfo.objects.get(id=nid)
            return render(request, '主页面.html', {'user': user})
        except models.Userinfo.DoesNotExist:
            # 如果用户不存在，清除session并重定向到登录页
            request.session.flush()#清除session
            return redirect('用户登入')
    else:
        # 如果session中没有用户信息，重定向到登录页
        return redirect('用户登入')

    # return redirect('用户登入')
    # # return render(request, '主页面.html',{'user': models.Userinfo.objects.filter(id=1).first()})
#修改页面
def settings(request):
    pass
#个人信息
def profile(request):
    nid = request.session.get('id')
    if id:
        try:
            user = models.Userinfo.objects.get(id=nid)
            return render(request, '个人资料.html', {'user': user})
        except models.Userinfo.DoesNotExist:
            # 如果用户不存在，清除session并重定向到登录页
            request.session.flush()#清除session
            return redirect('用户登入')
    else:
        # 如果session中没有用户信息，重定向到登录页
        return redirect('用户登入')
    # user = models.Userinfo.objects.get(id=nid)
    # return render(request, '个人资料.html', {'user': user})

#建立mysql的表
def orm(request):
    models.Userinfo.objects.create(name="米朝阳",Account="95330298",password="mijun214216",age=21,email="95330298@qq.com",
                                   gender="男")
    return HttpResponse("创建成功")

#清除 session
def user_log_out(request):
    """
       用户退出登录，清除session
       """
    # 清除所有session数据
    request.session.flush()

    # 可选：添加成功消息（需要配置messages中间件）
    # messages.success(request, "您已成功退出登录")

    # 重定向到登录页面
    return redirect('用户登入')
#######图片模块#######

# 个人图片列表
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import models
from .forms import PersonalPhotoForm
from django.http import HttpResponse, JsonResponse
import os

def personal_gallery(request):
    """个人相册主页"""
    # 检查用户是否登录 - 根据您的登录系统
    if 'id' not in request.session:
        messages.warning(request, '请先登录')
        return redirect('用户登入')  # 重定向到您的登录页面

    try:
        # 获取当前登录用户

        user_id = request.session['id']
        user = models.Userinfo.objects.get(id=user_id)

        # 获取该用户的照片
        photos = models.PersonalPhoto.objects.filter(user=user)

        # 获取统计信息
        total_count = photos.count()
        location_count = photos.values('location').distinct().count()

        # 获取年份范围
        if photos.exists():
            years = photos.dates('taken_date', 'year')
            year_count = len(years)
        else:
            year_count = 0

        context = {
            'photos': photos,
            'total_count': total_count,
            'location_count': location_count,
            'year_count': year_count,
            'form': PersonalPhotoForm()
        }

        return render(request, '图片存放.html',  { 'user':user,'context': context})

    except models.Userinfo.DoesNotExist:
        # 用户不存在，清除session并重定向到登录
        request.session.flush()
        messages.error(request, '用户不存在')
        return redirect('用户登入')
    except Exception as e:
        # 处理其他错误
        messages.error(request, f'加载相册时出错: {str(e)}')
        context = {
            'photos': [],
            'total_count': 0,
            'location_count': 0,
            'year_count': 0,
            'form': PersonalPhotoForm()
        }
        return render(request, '图片存放.html', context)


def upload_photo(request):
    """处理照片上传"""
    # 检查登录状态
    if 'id' not in request.session:
        return redirect('user_log_in')

    if request.method == 'POST':
        try:
            # 获取当前用户
            user_id = request.session['id']
            user = models.Userinfo.objects.get(id=user_id)

            form = PersonalPhotoForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.user = user  # 设置当前用户
                photo.save()
                messages.success(request, '照片上传成功！')
            else:
                messages.error(request, '请修正表单中的错误')

        except models.Userinfo.DoesNotExist:
            messages.error(request, '用户不存在')
        except Exception as e:
            messages.error(request, f'上传失败: {str(e)}')

    return redirect('personal_gallery')


# def delete_photo(request, photo_id):
#     """删除照片"""
#     # 检查用户是否登录
#     if 'id' not in request.session:
#         messages.warning(request, '请先登录')
#         return redirect('用户登入')
#
#     try:
#         # 获取当前登录用户
#         user_id = request.session['id']
#         user = models.Userinfo.objects.get(id=user_id)
#
#         # 获取要删除的照片，确保该照片属于当前用户
#         photo = get_object_or_404(models.PersonalPhoto, id=photo_id, user=user)
#
#         # 删除照片
#         photo.delete()
#         messages.success(request, '照片删除成功！')
#
#     except models.Userinfo.DoesNotExist:
#         messages.error(request, '用户不存在')
#     except models.PersonalPhoto.DoesNotExist:
#         messages.error(request, '照片不存在或您无权删除此照片')
#     except Exception as e:
#         messages.error(request, f'删除照片时出错: {str(e)}')
#
#     return redirect('personal_gallery')
# def delete_photo(request, photo_id):
#     """删除照片"""
#     # 检查用户是否登录
#     if 'id' not in request.session:
#         messages.warning(request, '请先登录')
#         return redirect('用户登入')
#
#     try:
#         # 获取当前登录用户
#         user_id = request.session['id']
#         user = models.Userinfo.objects.get(id=user_id)
#
#         # 获取要删除的照片，确保该照片属于当前用户
#         photo = get_object_or_404(models.PersonalPhoto, id=photo_id, user=user)
#
#         # 保存文件路径用于删除
#         photo_path = photo.image.path if photo.image else None
#
#         # 删除照片记录
#         photo.delete()
#
#         # 如果文件存在，尝试删除文件
#         if photo_path and os.path.exists(photo_path):
#             try:
#                 os.remove(photo_path)
#             except OSError as e:
#                 # 如果文件删除失败，记录错误但不影响主要功能
#                 print(f"删除文件失败: {e}")
#
#         messages.success(request, '照片删除成功！')
#
#     except models.Userinfo.DoesNotExist:
#         messages.error(request, '用户不存在')
#     except models.PersonalPhoto.DoesNotExist:
#         messages.error(request, '照片不存在或您无权删除此照片')
#     except Exception as e:
#         messages.error(request, f'删除照片时出错: {str(e)}')
#
#     return redirect('personal_gallery')
import os
import shutil
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from myapp import models
from django.contrib import messages
from myapp.models import Userinfo
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse


# ... 其他视图函数保持不变 ...

def delete_photo(request, photo_id):
    """删除照片及关联文件，并清理空文件夹"""
    # 检查用户是否登录
    if 'id' not in request.session:
        messages.warning(request, '请先登录')
        return redirect('用户登入')

    try:
        # 获取当前登录用户
        user_id = request.session['id']
        user = models.Userinfo.objects.get(id=user_id)

        # 获取要删除的照片，确保该照片属于当前用户
        photo = get_object_or_404(models.PersonalPhoto, id=photo_id, user=user)

        if photo.image:
            # 保存文件路径用于删除
            photo_path = photo.image.path
            # 获取文件所在目录，用于后续清理空文件夹
            file_dir = os.path.dirname(photo_path)

            # 删除数据库记录
            photo.delete()

            # 删除物理文件
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                    messages.success(request, '照片删除成功！')

                    # 清理空文件夹
                    cleanup_empty_directories(file_dir)

                except OSError as e:
                    messages.error(request, f'文件删除失败: {str(e)}')
            else:
                # 文件不存在，只删除数据库记录
                messages.success(request, '照片记录已删除，但文件不存在')
        else:
            # 如果没有文件，只删除数据库记录
            photo.delete()
            messages.success(request, '照片记录已删除')

    except models.Userinfo.DoesNotExist:
        messages.error(request, '用户不存在')
    except models.PersonalPhoto.DoesNotExist:
        messages.error(request, '照片不存在或您无权删除此照片')
    except Exception as e:
        messages.error(request, f'删除照片时出错: {str(e)}')

    # 如果是AJAX请求，返回JSON响应
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': '照片删除成功'})

    return redirect('personal_gallery')


def cleanup_empty_directories(start_dir):
    """
    递归清理空文件夹
    :param start_dir: 起始目录（文件所在目录）
    """
    try:
        # 获取项目根目录
        from django.conf import settings
        media_root = settings.MEDIA_ROOT
        personal_photos_dir = os.path.join(media_root, 'personal_photos')

        # 确保路径安全，只在 personal_photos 目录内操作
        if not os.path.abspath(start_dir).startswith(os.path.abspath(personal_photos_dir)):
            return

        current_dir = start_dir

        # 递归向上清理空目录，直到 personal_photos 目录
        while (os.path.exists(current_dir) and
               os.path.abspath(current_dir) != os.path.abspath(personal_photos_dir)):

            # 检查目录是否为空（排除隐藏文件）
            try:
                items = [item for item in os.listdir(current_dir)
                         if not item.startswith('.')]
            except OSError:
                # 如果无法访问目录，停止清理
                break

            if not items:  # 目录为空
                try:
                    os.rmdir(current_dir)
                    print(f"已删除空目录: {current_dir}")
                except OSError as e:
                    # 如果无法删除目录（如权限问题），停止清理
                    print(f"无法删除目录 {current_dir}: {e}")
                    break

                # 移动到父目录继续检查
                current_dir = os.path.dirname(current_dir)
            else:
                # 目录不为空，停止清理
                break

    except Exception as e:
        print(f"清理空目录时出错: {e}")
################
# 在 views.py 中添加以下函数
# 公共相册
# 在 views.py 中添加以下函数

def public_gallery(request):
    """公共相册 - 所有人都可以查看所有图片"""
    try:
        # 获取所有照片，按拍摄日期倒序排列
        photos = models.PersonalPhoto.objects.all().order_by('-taken_date')

        # 获取统计信息
        total_count = photos.count()
        location_count = photos.values('location').distinct().count()
        user_count = photos.values('user').distinct().count()

        # 获取年份范围
        if photos.exists():
            years = photos.dates('taken_date', 'year')
            year_count = len(years)
        else:
            year_count = 0

        # 获取所有用户信息用于显示
        users_with_photos = models.Userinfo.objects.filter(
            id__in=photos.values('user').distinct()
        )

        context = {
            'photos': photos,
            'total_count': total_count,
            'location_count': location_count,
            'year_count': year_count,
            'user_count': user_count,
            'users_with_photos': users_with_photos,
        }

        return render(request, '公共相册.html', context)

    except Exception as e:
        # 处理错误
        messages.error(request, f'加载公共相册时出错: {str(e)}')
        context = {
            'photos': [],
            'total_count': 0,
            'location_count': 0,
            'year_count': 0,
            'user_count': 0,
            'users_with_photos': [],
        }
        return render(request, '公共相册.html', context)


def user_photos(request, user_id):
    """查看特定用户的照片"""
    try:
        user = get_object_or_404(models.Userinfo, id=user_id)
        photos = models.PersonalPhoto.objects.filter(user=user).order_by('-taken_date')

        # 获取统计信息
        total_count = photos.count()
        location_count = photos.values('location').distinct().count()

        if photos.exists():
            years = photos.dates('taken_date', 'year')
            year_count = len(years)
        else:
            year_count = 0

        context = {
            'photos': photos,
            'user': user,
            'total_count': total_count,
            'location_count': location_count,
            'year_count': year_count,
        }

        return render(request, '用户相册.html', context)

    except Exception as e:
        messages.error(request, f'加载用户相册时出错: {str(e)}')
        return redirect('public_gallery')




