from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name="products"),
    url(r'^detail/(?P<pk>\d+)/$', detail, name="detail"),
    url(r'^traditional/$', Traditional.as_view(), name="traditional"),
    url(r'^formal/$', Formal.as_view(), name="formal"),
    url(r'^casual/$', Casual.as_view(), name="casual"),
    url(r'^ethnic/$', Ethnic.as_view(), name="ethnic"),
    url(r'^sports/$', Sports.as_view(), name="sports"),
    url(r'^western/$', Western.as_view(), name="western"),
    url(r'^tshirts/$', Tshirts.as_view(), name="tshirts"),
    url(r'^kids/$', Kids.as_view(), name="kids"),
    url(r'^jumpsuits/$', Jumpsuits.as_view(), name="jumpsuits"),
    url(r'^denim/$', Denim.as_view(), name="denim"),
    url(r'^myproducts/$', MyProductListView.as_view(), name="myproducts"),
    url(r'^edit/(?P<pk>\d+)/$', edit, name='edit'),
    url(r'^post/$', create, name='create'),
    url(r'^delete/(?P<pk>\d+)/$', delete, name='delete'),
    url(r'search/$', SearchList.as_view(), name='search'),
    url(r'^men/$', Men.as_view(), name="men"),
    url(r'^women/$', Women.as_view(), name="women"),

]