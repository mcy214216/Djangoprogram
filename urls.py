"""
URL configuration for myprogress project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from myapp import views
import myapp1.views as views1

# from myapp.views import upload_file, upload_multiple_files, advanced_upload

urlpatterns = [
#'''主界面'''------------------------------
    path("admin/", admin.site.urls),
    path( "", views.mcy),
    path( "main/", views.main,name='主页面'),
# '''用户'''---------------------------------
    path( "login/", views.user_log_in,name="用户登入"),
    path( "register/", views.user_register,name='用户注册'),
    # path( "settings/", views.settings,name='设置'),
    path( "profile/", views.profile,name='个人资料'),
    path( "logout/", views.user_log_out,name='用户退出'),
# '''数据库创建'''------------------------------
    path( "orm/", views.orm,name='创建数据库表'),
# '''图片模块'''------------------------------
    path('gallery/', views.personal_gallery, name='personal_gallery'),
    path('gallery/upload/', views.upload_photo, name='upload_photo'),
    path('gallery/delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
# '''公共相册'''------------------------------
    path('public-gallery/', views.public_gallery, name='public_gallery'),
    path('user-photos/<int:user_id>/', views.user_photos, name='user_photos'),

### 第二个app模块
    # path('cie/', views1.index, name='index'),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)