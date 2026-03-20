# 创建时间   : 2025/10/27 15:34
# 作者      : 叶之瞳
# 文件名     : forms.py
# forms.py
# forms.py
from django import forms
from .models import PersonalPhoto

class PersonalPhotoForm(forms.ModelForm):
    class Meta:
        model = PersonalPhoto
        fields = ['title', 'image', 'taken_date', 'location', 'description', 'camera', 'tags', 'category']
        widgets = {
            'taken_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': '描述这张照片的故事...'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '给照片起个标题'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '拍摄的具体地点'
            }),
            'camera': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '使用的拍摄设备'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例如：旅行, 自然, 风景'
            }),
        }