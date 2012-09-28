#from django.conf.urls import patterns, include, url
#from mysite.views import hello,current_datetime,hours_ahead,my_homepage_view
from django.conf.urls.defaults import *
from views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    
    ('^$', my_homepage_view),
    ('^hello$', hello),
    ('^date$',current_datetime),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    (r'^latest/$', latest_books),
    (r'^current_bad/$', current_url_view_bad),
    (r'^current_good/$', current_url_view_good),
    (r'^ua_bad/$', ua_display_bad),
    (r'^ua_good1/$', ua_display_good1),
    (r'^ua_good2/$', ua_display_good2),
    (r'^display_meta/$', display_meta),
    (r'^search_form/$', search_form),
    (r'^search/$', search),
    #(r'^bad_search/$', bad_search),
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
)