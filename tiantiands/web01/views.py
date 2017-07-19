from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from  web01.models import *
from statics.plugin.captcha import captcha
import redis
from hashlib import md5
from web01 import user_decoder
from django.db import transaction
from datetime import datetime


def redisdb():
    return redis.StrictRedis(host='localhost', port=6379)
def regist(request):
    print('regist')
    return  render(request,'user/regist.html', {'title': '注册'})
def login(request):
    print(request.COOKIES)
    print(request.session.keys(), request.session.items())
    name = request.COOKIES.get('uname', '')
    context = {'title': '登录', 'error_name':3, 'error_passwd':3, 'name':name, 'passwd':''}
    return  render(request,'user/login.html', context)

def generate_code(request):
    print('获取图片验证码')
    rd = redisdb()

    """获取图片验证码"""
    # 生成图片验证码
    cp = captcha.Captcha.instance()

    name, text, pic_data = cp.generate_captcha()
    rd.setex('code', 60, text.upper())

    print(name, text, type(name), type(text))
    return HttpResponse(pic_data)

def registCheckHandle(request):
    post = request.GET
    name = post.get('user_name')

    user = userInfo.objects.filter(uname=name).first()
    if user:
        '''用户存在'''
        print('用户存在')
        return JsonResponse({'count': 1})
    return JsonResponse({'count':None})

def registHandle(request):
    post = request.POST
    name = post.get('user_name')
    passwd = post.get('pwd')
    email = post.get('email', None)

    md = md5()
    md.update(passwd.encode('utf-8'))
    passwd1 = md.hexdigest()

    user = userInfo()
    user.uname = name
    user.upasswd = passwd1
    user.uemail = email
    user.save()

    return redirect('/user/login/')

def loginHandle(request):
    post = request.POST

    name = post.get('username')
    passwd = post.get('pwd')
    code = post.get('code', None)
    auto_box = post.get('auto_box', None)
    print(name, passwd, code, type(code), auto_box, type(auto_box),'------box----')

    md = md5()
    md.update(passwd.encode('utf-8'))
    passwd1 = md.hexdigest()

    if code:
        rd = redisdb()
        code1 = rd.get('code').decode()
        print(code1, type(code1),'---------')
        user = userInfo.objects.filter(uname=name).first()
        context = {'title': '登录', 'error_user': 1, 'error_passwd': 3, 'name': name, 'passwd': passwd}
        if code.upper() == code1 and user:
            context['error_user'] = 3
            context['error_passwd'] = 1
            if user.upasswd == passwd1:
                '''login success'''
                context['error_passwd'] = 3

                redict_url = request.COOKIES.get('url', '/index/')
                red = HttpResponseRedirect(redict_url)

                if auto_box == 'on':
                    print('auto login on')
                    print(request.COOKIES)
                    
                    red.set_cookie('uname', name)
                    # red.set_cookie('upasswd', passwd)
                else:
                    red.set_cookie('uname', '', max_age=-1)
                    # red.set_cookie('upasswd', '', max_age=-1)

                request.session['user_id'] = user.id
                request.session['user_name'] = name
                return red

        return render(request, 'user/login.html', context)
    else:
        user = userInfo.objects.filter(uname=name).first()
        # print(user, user.upasswd, passwd1)
        context = {'title': '登录', 'error_user': 1, 'error_passwd': 3, 'name': name, 'passwd': passwd}
        if user:
            context['error_user'] = 3
            context['error_passwd'] = 1
            if user.upasswd == passwd1:
                '''login success'''
                context['error_passwd'] = 3

                redict_url = request.COOKIES.get('url', '/index/')
                red = HttpResponseRedirect(redict_url)
                if auto_box == 'on':
                    print('auto login on')
                    print(request.COOKIES)
                    red.set_cookie('uname', name)
                    # red.set_cookie('upasswd', passwd)
                else:
                    red.set_cookie('uname', '', max_age=-1)
                    # red.set_cookie('upasswd', '', max_age=-1)
                request.session['user_id'] = user.id
                request.session['user_name'] = name
                return red

        return render(request, 'user/login.html', context)

@user_decoder.user
def user_center(request):
    name = request.session.get('user_name', '')
    uid = request.session.get('user_id', 1)

    user = userInfo.objects.get(id = uid)

    p_list = []
    ids = request.COOKIES.get('good_ids', '')
    id_list = ids.split(',')
    for pid in id_list:
        p = product.objects.get(id = pid)
        p_list.append(p)

    print(p_list, p_list[0].__dict__)
    contex = {'user':user, 'goods':p_list,'name':name, 'phone':user.uphone, 'address':user.uaddress, 'email':user.uemail, 'title':'用户中心'}
    return render(request, 'user/user_center_info.html', contex)
@user_decoder.user
def centerOrder(request):
    uid = request.session.get('user_id')
    user = userInfo.objects.get(id = uid)

    paid_orders = orderInfo.objects.filter(uid = uid, isPaid=True).order_by('-r_time')
    not_paid_orders = orderInfo.objects.filter(uid = uid, isPaid=False).order_by('-r_time')

    return render(request, 'user/user_center_order.html', {'title':'用户中心', 'user': user, 'paid_orders':paid_orders, 'not_paid_orders':not_paid_orders})
@user_decoder.user
def centerSite(request):
    uid = request.session.get('user_id')
    if request.method == 'POST':
        post = request.POST
        name = post.get('name', '')
        address = post.get('address', '')
        phone = post.get('phone')
        youbian = post.get('youbian')

        user = userInfo.objects.get(id = uid)
        user.shouname = name
        user.uaddress = address
        user.uphone = phone
        user.uyoubian = youbian
        user.save()

    userinfo = userInfo.objects.get(id=uid)
    print(userinfo, userinfo.__dict__)
    return render(request, 'user/user_center_site.html', {'user': userinfo, 'title':'用户中心'})
@user_decoder.user
def payorder(request):
    uid = request.session.get('user_id')

    gids = request.GET.get('gids')
    gids_list = gids.split('-')
    print(gids,'-----------',gids_list)

    goods = []
    total_price = gids_list.pop()
    for pid in gids_list:
        good = cart.objects.get(uid=uid, pid=pid)
        goods.append(good)

    userinfo = userInfo.objects.get(id=uid)
    url = request.get_full_path()
    url_list = url.split('/')
    last = url_list.pop()
    start = last.index('=')
    print(last, 'url', start, last[start+1:])
    return render(request, 'product/place_order.html', {'url':last[start+1:],'total': total_price + str(10),'user': userinfo, 'title':'提交订单', 'goods':goods, 'count':len(goods)})

@user_decoder.user
def payOrder(request, pid, count):
    print(pid, count,'单一商品购买通道-进去提价订单页面')
    uid = request.session.get('user_id')
    userinfo = userInfo.objects.get(id=uid)

    carts = cart.objects.filter(uid=uid, pid=pid)
    if len(carts) >= 1:
        '''商品已经存在'''
        c = carts[0]
        c.count += int(count)
    else:
        c = cart()
        c.uid = userinfo
        c.pid = product.objects.get(id=pid)
        c.count = count
    c.save()

    pdt = cart.objects.get(pid = pid, uid=uid)
    # print(pdt.price, type(pdt.price), pdt.price*2)

    total = pdt.pid.price * int(pdt.count)
    # return redirect('/product/cart/')
    return render(request, 'product/place_order.html', {'url':pid + '-' + str(total),'total': total,'user':userinfo, 'goods':[pdt,], 'count':count, 'title':'提交订单'})

@transaction.atomic()
def submitOrder(request):
    # '/product/submitOrder/?gids=7-4-70.80';
    '''创建原子性操作开始节点'''
    start_Tag = transaction.savepoint()

    try:
        uid = request.session.get('user_id')
        user = userInfo.objects.get(id=uid)
        gids = request.GET.get('gids')
        print('---1------', gids)
        # start = gids.index('=')
        # gids = gids[start+1:]
        gids_list = gids.split('-')
        print(gids, '-----submitOrder------', gids_list)

        goods = []
        total_price = gids_list.pop()
        for pid in gids_list:
            good = cart.objects.get(uid=int(uid), pid=int(pid))
            goods.append(good)
        print('---------------', type(uid))
        '''创建订单'''
        orderinfo = orderInfo()
        now = datetime.now()
        orderinfo.orderNumber = now.strftime('%Y%m%d%H%M%S') + str(uid)

        orderinfo.uid = user
        orderinfo.total_price = total_price
        orderinfo.isPaid = True
        orderinfo.save()
        print('-------2--------')
        for item in goods:
            '''清理购物车'''
            cart.objects.get(id=item.id).delete()
            '''清理库存'''
            p = product.objects.get(id=item.pid.id)
            if p.stock >= item.count:
                p.stock -= item.count
            else:
                raise ValueError('您购买的商品数量超出库存。')
            p.save()
            '''保存订单对应商品'''
            orderdetail = orderProInfo()
            orderdetail.order = orderinfo
            orderdetail.pid = item.pid
            orderdetail.count = item.count
            orderdetail.price = item.pid.price
            orderdetail.save()

        transaction.savepoint_commit(start_Tag)#若没有错误，则保存原子操作中所有数据集
    except Exception as e:
        print('提交订单失败：',e)
        '''倘若一步出错取不取消并且回滚到最初状态'''
        transaction.savepoint_rollback(start_Tag)

    return redirect('/user/centerOrder/')
def index(request):

    goods = product.objects.filter(category__name='新鲜水果', isDelete=0).order_by('-hots')[0:4]
    print(goods)
    return render(request, 'product/index.html', {'title':'首页','request': request, 'goods':goods})

def detail(request, pid):
    print(pid, type(pid))

    good = product.objects.get(id= pid)
    good.hots += 1
    good.save()

    new = product.objects.order_by('-id')[0:2]
    # print(new,)
    conmentss = good.conment_set.all()
    conments = conment.objects.filter(pid= pid).values('uid__uname', 'content', 'r_time')
    print((conments), '\n', conmentss, good)

    response = render(request, 'product/detail.html', {'request': request, 'good':good, 'new':new, 'cmts':conments})
    goods_id = request.COOKIES.get('good_ids', '')
    if goods_id !='':
        id_list = goods_id.split(',')
        if id_list.count(pid) >= 1:
            id_list.remove(pid)

        id_list.insert(0, pid)
        if len(id_list) > 5:
            del id_list[5]
        goods_id = ','.join(id_list)
        print(goods_id, id_list)
        response.set_cookie('good_ids', goods_id)
    else:
        goods_id = pid
        response.set_cookie('good_ids', goods_id)

    return response

def product_list(request, category, sort, pageNum):
    print(category, sort, type(sort))
    new = product.objects.order_by('-id')[0:2]

    if sort == '2':
        '''人气'''
        goods = product.objects.filter(category__name='新鲜水果', isDelete=0).order_by('-hots')

    elif sort == '1':
        '''价格'''
        goods = product.objects.filter(category__name='新鲜水果', isDelete=0).order_by('-price')
    else:
        '''默认'''
        goods = product.objects.filter(category__name='新鲜水果', isDelete=0).order_by('-weight')

    p = Paginator(goods, 2)
    pro_list = p.page(pageNum)
    num_list = p.page_range
    print(p, p.__dict__, num_list, pro_list.has_next(), pro_list.has_previous())
    contex = {'title':'商品列表','curr_page':pageNum, 'request':request, 'category':category,'sort':sort,'goods':pro_list,'new':new,'num_list':num_list}
    return render(request, 'product/list.html', contex)

@user_decoder.user
def cartStore(request):
    uid = request.session.get('user_id')
    userinfo = userInfo.objects.get(id=uid)

    carts = cart.objects.filter(uid=uid).order_by('-id')

    contex = {'user': userinfo, 'goods':carts, 'title':'购物车'}
    return render(request, 'product/cart.html', contex)
@user_decoder.user
def logout(request):

    # request.session['user_name'] = ''
    # request.session['user_id'] = ''
    # del request.session['user_name']
    # 用户session的随机字符串
    # request.session.session_key
    # 将所有Session失效日期小于当前日期的数据删除
    # request.session.clear_expired()
    # 检查 用户session的随机字符串 在数据库中是否
    # request.session.exists("session_key")
    # 删除当前用户的所有Session数据
    # request.session.delete("session_key")
    # request.session.set_expiry(value)

    request.session.flush()
    print(request.session.keys, 'session')
    request.COOKIES.clear()
    print(request.COOKIES.values(),'cookies')
    return redirect('/user/login/')
@user_decoder.user
def add2card(request, pid, count):
    uid = request.session.get('user_id')
    user = userInfo.objects.get(id=uid)
    p = product.objects.get(id=pid)

    carts = cart.objects.filter(uid=uid, pid=pid)
    if len(carts) >= 1:
        '''商品已经存在'''
        c = carts[0]
        c.count += int(count)
    else:
        c = cart()
        c.uid = user
        c.pid = p
        c.count = count
    c.save()

    if request.is_ajax():
        count = cart.objects.filter(uid=uid).count()

        return JsonResponse({'count': count})
    else:

        # carts = cart.objects.filter(uid=uid).order_by('-id')
        # contex = {'user': user, 'goods': carts, 'title': '购物车'}
        # return render(request, 'product/cart.html', contex)由于请求的URL未变此种方式会造成用户刷新页面购物车自动增加商品
        return redirect('/product/cart/')
@user_decoder.user
def delcart(request, pid):
    uid = request.session.get('user_id')
    user = userInfo.objects.get(id=uid)
    p = product.objects.get(id=pid)

    try:
        cart.objects.get(uid=user, pid=p).delete()
        return JsonResponse({'state':True})
    except Exception as e:
        return JsonResponse({'state': True, 'error':e})
        print('删除购物车商品失败：', e)
@user_decoder.user
def getCartCount(request):
    uid = request.session.get('user_id')
    count = cart.objects.filter(uid=uid).count()

    return JsonResponse({'count': count})
@user_decoder.user
def editcart(request, pid, count):
    uid = request.session.get('user_id')
    # user = userInfo.objects.get(id=uid)
    # p = product.objects.get(id=pid)
    try:
        good = cart.objects.get(uid=uid, pid=pid)
        good.count = count
        good.save()
        return JsonResponse({'status':True})
    except Exception as e:
        return JsonResponse({'status': False, 'error':e})

from haystack.views import SearchView

class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '商品搜索结果'

        return context


