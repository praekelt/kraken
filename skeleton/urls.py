from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', 'kraken.views.index', name='home'),

    # Projects
    url(r'^profile/$', 'kraken.views.profiles_index', name='profiles_index'),
    #url(r'^profile/create$', 'kraken.views.profiles_create', name='profiles_create'),
    #url(r'^profile/edit/(?P<id>[\w-]+)$', 'kraken.views.profiles_edit', name='profiles_edit'),
    #url(r'^profile/view/(?P<id>[\w-]+)$', 'kraken.views.profiles_view', name='profiles_view'),

    # Authentication
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
    url(r'^accounts/profile/$', 'kraken.views.accounts_profile', name='accounts_profile'),

    #url(r'', include('social_auth.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
