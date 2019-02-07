from django.conf.urls import url, include
from .views import *
from Products.views import SearchList1

urlpatterns =[
    url(r'^$', home, name='home'),
    url(r'^search1/$', SearchList1.as_view(), name="search1"),
    url(r'^contact/$', contact, name="contact"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/$', profile, name="profile"),
    url(r'^profile/edit/', editProfile, name="profile_edit"),
    url(r'^profile/delete/(?P<pk>\d+)/$', deleteProfile, name="profile_delete"),
    url(r'^help/', help, name='help'),
    url(r'^products/', include('Products.urls')),
    url(r'^feedback/', Feedback, name='feedback'),
    url(r'^cart/', include('Cart.urls', namespace="cart")),
    url(r'^how-it-work/', Howitworks, name='how_it_work'),
    url(r'^about-us/', aboutus, name='about_us'),
    url(r'^location/', location, name='location'),
    url(r'^location/', location, name='location'),

]