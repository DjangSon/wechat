from django.conf.urls import url
from web import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^subscription/', views.subscription),
    url(r'^wechat_list/', views.wechat_list),
    url(r'^add_page/', views.add_page),
    url(r'^add_wechat', views.add_wechat),
    url(r'^get_access_token/', views.get_access_token),
    url(r'logout/', views.logout),
]
