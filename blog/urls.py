# coding:utf-8
from django.conf.urls import url
from . import views



app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
]

# #Django 使用正则表达式来匹配用户访问的网址。这里 r'^post/(?P<pk>[0-9]+)/$' 整个正则表达式刚好匹配我们上面定义的 URL 规则。这条正则表达式的含义是，以 post/ 开头，后跟一个至少一位数的数字，并且以 / 符号结尾，如 post/1/、 post/255/ 等都是符合规则的，[0-9]+ 表示一位或者多位数。此外这里 (?P<pk>[0-9]+) 表示命名捕获组，其作用是从用户访问的 URL 里把括号内匹配的字符串捕获并作为关键字参数传给其对应的视图函数 detail。