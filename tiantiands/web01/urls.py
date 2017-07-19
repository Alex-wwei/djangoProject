from django.conf.urls import url

from web01 import views

urlpatterns = [
    url(r'^regist/$', views.regist),
    url(r'^login/$', views.login),
    url(r'^usercenter/$', views.user_center),
    url(r'^centerOrder/$', views.centerOrder),
    url(r'^centerSite/$', views.centerSite),
    url(r'^veryfyCode/', views.generate_code),
    url(r'^regist_handler/$', views.registHandle),
    url(r'^regist_check_handler/$', views.registCheckHandle),
    url(r'^login_handler/$', views.loginHandle),
    url(r'^payorder/$', views.payorder),
    url(r'^submitOrder/$', views.submitOrder),
    url(r'^detail/(\d+)$', views.detail),
    url(r'^list-(\d+)-(\d+)-(\d+)$', views.product_list),
    url(r'^cart/$', views.cartStore),
    url(r'^add2cart/(\d+)/(\d+)/$', views.add2card),
    url(r'^editcart/(\d+)/(\d+)/$', views.editcart),
    url(r'^delcart/(\d+)/$', views.delcart),
    url(r'^logout/$', views.logout),
    url(r'^getCartCount/$', views.getCartCount),

]