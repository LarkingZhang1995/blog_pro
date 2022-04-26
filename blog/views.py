# coding:utf-8
import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# Create your views here.

# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list})

# 将 index 视图函数改写为类视图

class IndexView(ListView):
    model = Post # 将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
    template_name = 'blog/index.html' # 指定这个视图渲染的模板。
    context_object_name = 'post_list' # 指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。
    paginate_by = 2 # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章 而类视图 ListView 已经帮我们写好了上述的分页逻辑，我们只需通过指定 paginate_by 属性来开启分页功能即可，即在类视图中指定 paginate_by 属性的值


    def get_context_data(self, **kwargs):
        # 首先获得父类生成的传递给模板的字典。
        context = super(IndexView,self).get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context


# index 视图函数首先通过 Post.objects.all() 从数据库中获取文章（Post）列表数据，并将其保存到 post_list 变量中。而在类视图中这个过程 ListView 已经帮我们做了。
# 只需告诉 ListView 去数据库获取的模型是 Post，而不是 Comment 或者其它什么模型，即指定 model = Post
# 将获得的模型数据列表保存到 post_list 里，即指定 context_object_name = 'post_list'
# index 视图函数中使用 render 函数。但这个过程 ListView 已经帮我们做了，我们只需指定渲染哪个模板即可
# 好在将类视图转换成函数视图非常简单，只需调用类视图的 as_view() 方法即可,匹配路由使用 views.IndexView.as_view()


#---------------------------------
# 第 1 页页码，这一页需要始终显示。
# 第 1 页页码后面的省略号部分。但要注意如果第 1 页的页码号后面紧跟着页码号 2，那么省略号就不应该显示。
# 当前页码的左边部分，比如这里的 3-6。
# 当前页码，比如这里的 7。
# 当前页码的右边部分，比如这里的 8-11。
# 最后一页页码前面的省略号部分。但要注意如果最后一页的页码号前面跟着的页码号是连续的，那么省略号就不应该显示。
# 最后一页的页码号。

    def pagination_data(self, paginator, page, is_paginated):
        # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
        if not is_paginated:
            return {}
        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号
        # 因为如果当前页左边的连续页码号中已经含有第1页的页码号，此时就无需再显示第1页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False
        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False
        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages
        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = []
        if total_pages > 1:
            for num in xrange(1,total_pages+1):
                page_range.append(num)
        else:
            page_range = [1]
        # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）
        if page_number == 1:
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True
            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True
        # 如果用户请求的是最后一页的数据，那么当前页右边的不需要数据，因此 right=[]（已默认为空）
        elif page_number == total_pages:
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后前面两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1] #[1, 2, 3, 4] 获取 [2,3], [1,2,3] 获取 [1,2]
            # 如果最左边的页码号比第一页的页码号加上1还要大，
            # 说明最左边的页码号和第一页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True
            # 如果最左边的页码号比第一页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            # 是否需要显示第一页后和最后一页前的省略号 [1,2,3,4,5,6]
            if left[0] > 2:
                left_has_more = True
            if right[-1] < total_pages -1:
                right_has_more = True

            #是否显示第一页和最后一页
            if left[0] > 1:
                first = True
            if right[-1] < total_pages:
                last = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data






















        #-----------------------------------------------------------------------------
# def detail(request,pk):
#     post = get_object_or_404(Post, pk=pk)
#     # 阅读量 +1
#     # 当用户请求访问某篇文章时，处理该请求的视图函数为detail 。一旦该视图函数被调用，说明文章被访问了一次，因此我们修改 detail 视图函数，让被访问的文章在视图函数被调用时阅读量 + 1。
#     post.increase_views()
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                       ])
#     form = CommentForm()
#     # 获取这篇 post 下的全部评论
#     comment_list = post.comment_set.all()
#
#     # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request, 'blog/detail.html', context=context)



class PostDetailView(DetailView):
    model = Post  # 将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。
    template_name = 'blog/detail.html'  # 指定这个视图渲染的模板。
    context_object_name = 'post'  # 指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。
    # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
    # get 方法返回的是一个 HttpResponse 实例
    # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
    # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
    def get(self,request,*args,**kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()# 阅读量 +1. 注意 self.object 的值就是被访问的文章 post

        return response
    # 渲染相应数据
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify)
        ])
        post.body = md.convert(post.body)
        # 而一旦调用该方法后，实例md就会多出一个toc属性，这个属性的值就是内容的目录，我们把md.toc的值赋给post.toc属性（要注意这个
        # post实例本身是没有 md属性的，我们给它动态添加了md属性，这就是Python动态语言的好处，不然这里还真不知道该怎么把oc的值传给模板）。
        post.toc = md.toc
        return post


    # 获取这篇文章下的全部评论
    # 最后我们复写了
    # get_context_data
    # 方法。这部分对应着
    # detail
    # 视图函数中生成评论表单、获取
    # post
    # 下的评论列表的代码部分。这个方法返回的值是一个字典，这个字典就是模板变量字典，最终会被传递给模板。
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context








# def archives(request,year,month):
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

# 将 archives 视图函数改写成类视图
class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,created_time__month=month)


# class ArchivesView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#
#     def get_queryset(self):
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')
#         return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
#                                                                created_time__month=month
#                                                                )

# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

# 将 category 函数改写成类视图 可先直接继承IndexView
#和 IndexView 不同的地方是，我们覆写了父类的 get_queryset 方法 ,该方法默认获取指定模型的全部列表数据
#首先是需要根据从 URL 中捕获的分类 id（也就是 pk）获取分类，这和 category 视图函数中的过程是一样的。
# 不过注意一点的是，在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，非命名组参数值保存在实例的 args 属性（是一个列表）里。
# 所以我们使了 self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值。
# 然后我们调用父类的 get_queryset 方法获得全部文章列表，紧接着就对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回。
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


