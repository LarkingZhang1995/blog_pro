# coding:utf-8
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta: # 表单内部类
        model = Comment
        fields = ['name', 'email', 'url', 'text']