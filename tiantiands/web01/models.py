from django.db import models
from tinymce.models import  HTMLField


# @transaction.atomic()
class userInfo(models.Model):

    uname = models.CharField(max_length=16, verbose_name='用户名', unique=True)
    upasswd = models.CharField(max_length=32, verbose_name='密码')
    uemail = models.CharField(max_length=32, verbose_name='邮箱')

    shouname = models.CharField(max_length=16, verbose_name='收件人')
    uyoubian = models.CharField(max_length=6, verbose_name='邮编')
    uaddress = models.CharField(max_length=100, verbose_name='地址')
    uphone = models.CharField(max_length=11, verbose_name='手机')

    u_time = models.DateTimeField(auto_now=True, null=False, verbose_name='更新时间')
    r_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='注册时间')

    def __str__(self):
        return self.uname

class product(models.Model):

    title = models.CharField(max_length=50, verbose_name='商品名称')
    description = models.CharField(max_length=200,verbose_name='商品描述')
    detail = HTMLField()#富文本
    standard = models.CharField(max_length=10, verbose_name='规格', default='500g')
    price = models.DecimalField(max_digits=5, decimal_places=2, null = False,verbose_name='单价')
    hots = models.IntegerField(default=0, verbose_name='热度')#销量
    weight = models.IntegerField(default=0, verbose_name='权重')
    icon_url = models.ImageField(upload_to='productsIcon/', null=True)
    isDelete = models.BooleanField(default=False)
    stock = models.IntegerField(default=100)

    uid = models.ForeignKey(userInfo)
    category = models.ForeignKey('category')

    u_time = models.DateTimeField(auto_now=True, null=False, verbose_name='更新时间')
    r_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='添加时间')

    def __str__(self):
        return self.title

class cart(models.Model):

    pid = models.ForeignKey(product)
    uid = models.ForeignKey(userInfo)
    count = models.IntegerField(default=1)
    isDelete = models.BooleanField(default=False)

    r_time = models.DateTimeField(auto_now=True, null=False, verbose_name='添加时间')

    class Meta:
        unique_together = ('pid', 'uid',)
        verbose_name_plural = '购物车'

class orderInfo(models.Model):


    orderNumber = models.CharField(max_length=32, primary_key=True)
    uid = models.ForeignKey(userInfo)

    total_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='总价')
    address = models.CharField(max_length=150)

    isDelete = models.BooleanField(default=False)
    isConment = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False, verbose_name='是否付款')

    r_time = models.DateTimeField(auto_now=True, verbose_name='生成时间')

class orderProInfo(models.Model):

    pid = models.ForeignKey(product)
    order = models.ForeignKey(orderInfo)

    count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, verbose_name='单价')


# class recent_views(models.Model):
#     pid = models.ForeignKey(product)
#     uid = models.ForeignKey(userInfo)
#
#     class Meta:
#         unique_together = ('pid', 'uid',)

class conment(models.Model):

    uid = models.ForeignKey(userInfo)
    content = models.CharField(max_length=120, verbose_name='评论')
    pid = models.ForeignKey(product)

    r_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name='时间')

    def __str__(self):
        return self.content

class category(models.Model):
    name = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class detail_ctg(models.Model):
    name = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)

    category_id = models.ForeignKey(category)







