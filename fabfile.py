# coding:utf-8
from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "https://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@github.com/LarkingZhang1995/blog_pro.git"

env.user = 'root'
env.password = 'Akaishi2022.'

# 填写你自己的主机对应的域名
env.hosts = ['myblog2.fun']

# 一般情况下为 22 端口，如果非 22 端口请查看你的主机服务提供商提供的信息
env.port = '22'


def deploy():
    source_folder = '/home/zhuifeng/sites/myblog2.fun/blog_pro'

    run('cd %s && git pull' % source_folder)
    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python manage.py collectstatic --noinput &&
        ../env/bin/python manage.py migrate
        """.format(source_folder))
    sudo('systemctl restart blog_pro')
    sudo('service nginx reload')