#coding:utf-8
from ..models import Post, Category,Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()

# 最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


# 归档模板标签 按月归档
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板标签
@register.simple_tag
def get_categories():
    # return Category.objects.all()
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
# 这个 Category.objects.annotate 方法和 Category.objects.all 有点类似，它会返回数据库中全部 Category 的记录，
# 但同时它还会做一些额外的事情，在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。代码中的 Count 方法为我们做了这个事，
# 它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，
# 也就是文章数，最后把这个值保存到 num_posts 属性中。此外，我们还对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉。
# 因为 num_posts 的值小于 1 表示该分类下没有文章，没有文章的分类我们不希望它在页面中显示。关于 filter 函数以及查询表达式（双下划线）在之前已经讲过，具体请参考 分类与归档

@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    # 获取到文章数大于0的标签列表，然后在模板中渲染显示它。
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
