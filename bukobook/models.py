from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Userinfo(AbstractUser):
    first_name = None
    last_name = None
    publish = models.IntegerField(default=0)  #: 发表数
    attention = models.IntegerField(default=0)  #: 关注数
    follower = models.IntegerField(default=0)  #: 粉丝数
    collection = models.IntegerField(default=0)  #: 收藏数
    nickname = models.CharField(max_length=10, blank=True)  #: 昵称可空
    intro = models.TextField(max_length=100, blank=True)  #: 简介可空
    phone_number = models.CharField('phone number', max_length=13, blank=True)  #: 手机号

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog.personal', args=[str(self.id)])


class Article(models.Model):
    tag_type = (
        ('R', 'reprint'),
        ('O', 'original'),
    )
    author = models.ForeignKey(Userinfo, on_delete=models.CASCADE)  #: 用户一对多
    title = models.CharField(max_length=20)  #: 文章标题
    body = models.TextField()  #: 文章主体
    follower = models.IntegerField(default=0)  #: 收藏者
    liker = models.IntegerField(default=0)  #: 喜欢者
    pv = models.IntegerField('page blog', default=0)  #: page_view 浏览量
    tag = models.CharField(max_length=1, choices=tag_type)  #: 标签
    create_time = models.DateTimeField('date published', auto_now_add=True)
    comments = models.IntegerField('comment count', default=0) #: 评论数

    def __str__(self):
        return self.title

    def is_hot_article(self):
        return 300 < self.pv or 100 < self.liker or 30 < self.follower

    class Meta:
        ordering = ['-create_time']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  #: 文章一对多
    author = models.ForeignKey(Userinfo, on_delete=models.CASCADE, default=None)
    body = models.TextField(max_length=180)  #: 评论主体
    floor = models.IntegerField(default=0)  #: 评论楼层
    create_time = models.DateTimeField('date published', auto_now_add=True)  #: 创造时间
    liker = models.IntegerField(default=0)  #: 点赞数
    reply_to = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.body

    def is_hot_comment(self):
        return 100 < self.liker

    class Meta:
        ordering = ['article', 'floor', 'create_time']
