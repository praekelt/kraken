from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', 'kraken.views.index', name='home'),

    # Profiles
    url(r'^profile/$', 'kraken.views.profile_index', name='profile_index'),
    url(r'^profile/create$', 'kraken.views.profile_create', name='profile_create'),
    url(r'^profile/(?P<id>[\w-]+)/edit$', 'kraken.views.profile_edit', name='profile_edit'),
    url(r'^profile/(?P<id>[\w-]+)$', 'kraken.views.profile_view', name='profile_view'),

    url(r'^profile/(?P<id>[\w-]+)/add_agent$', 'kraken.views.profile_add_agent', name='profile_add_agent'),

    url(r'^profile/(?P<id>[\w-]+)/add_request$', 'kraken.views.profile_add_request', name='profile_add_request'),
    url(r'^profile/(?P<id>[\w-]+)/edit_request/(?P<rid>[\w-]+)$', 'kraken.views.profile_edit_request', name='profile_edit_request'),
    url(r'^profile/(?P<id>[\w-]+)/delete_request/(?P<rid>[\w-]+)$', 'kraken.views.profile_delete_request', name='profile_delete_request'),

    url(r'^profile/(?P<id>[\w-]+)/run$', 'kraken.views.profile_run', name='profile_run'),

    # Tests
    url(r'^profile/report/(?P<id>[\w-]+)$', 'kraken.views.test_report', name='test_report'),

    # Servers
    url(r'^servers/$', 'kraken.views.server_index', name='server_index'),
    url(r'^servers/create$', 'kraken.views.server_create', name='server_create'),
    url(r'^servers/(?P<id>[\w-]+)/edit$', 'kraken.views.server_edit', name='server_edit'),

    # Agents
    url(r'^agent/create/(?P<id>[\w-]+)$', 'kraken.views.agent_create', name='agent_create'),

    # Authentication
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
    url(r'^accounts/profile/$', 'kraken.views.accounts_profile', name='accounts_profile'),

    url(r'', include('social_auth.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
