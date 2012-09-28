from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('ProcurementApp.views',
    # Examples:
    # url(r'^$', 'Procurement.views.home', name='home'),
    # url(r'^Procurement/', include('Procurement.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^main/$','main'),
    url(r'^main/import/$','dataimport'),
    url(r'^main/operate/$','operate'),
    #url(r'^main/import/file/$','dataimport_file'),
    url(r'^main/operate/category/(.+?)/$','operate'),
    url(r'^main/operate/ASIN/(.+?)/$','operateDetail'),
)
