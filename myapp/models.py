from django.db import models
from django.utils import timezone
import os
from django.contrib.auth.models import User

# Create your models here.
######用户信息模块####
class Userinfo(models.Model):
    id = models.AutoField(primary_key=True)#主键
    name = models.CharField(max_length=32)#用户名
    Account = models.CharField(max_length=32)#账号
    password = models.CharField(max_length=64)#密码
    age = models.IntegerField(default=2)#年龄
    email = models.EmailField()#邮箱
    # gender = models.CharField(max_length=10)# 性别
    gender = models.CharField(
        max_length=10,
        default='unknown',  # 默认值
    )


###########图片模块######
class PersonalPhoto(models.Model):
    CATEGORY_CHOICES = [#分类选项
        ('travel', '旅行'),
        ('family', '家庭'),
        ('friends', '朋友'),
        ('nature', '自然'),
        ('other', '其他'),
    ]

    # 修改这里：使用您的Userinfo模型
    user = models.ForeignKey(
        Userinfo,
        on_delete=models.CASCADE,
        verbose_name="用户",
        db_column='user_id'  # 显式指定数据库列名
    )
    title = models.CharField(max_length=200, verbose_name="照片标题")
    image = models.ImageField(upload_to='personal_photos/%Y/%m/', verbose_name="照片文件")
    description = models.TextField(blank=True, verbose_name="照片描述")
    taken_date = models.DateField(verbose_name="拍摄日期")
    location = models.CharField(max_length=200, verbose_name="拍摄地点")

    camera = models.CharField(max_length=100, blank=True, verbose_name="拍摄设备")
    tags = models.CharField(max_length=300, blank=True, verbose_name="标签")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name="分类")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "个人照片"
        verbose_name_plural = "个人照片"
        ordering = ['-taken_date']

    def __str__(self):
        return self.title

    @property
    def tags_list(self):
        """将标签字符串转换为列表"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []