from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from kraken import models


# There's no easy way to stub out the celery task, so we neuter it by using
# /usr/bin/true as the tsung executable.
@override_settings(
    CELERY_ALWAYS_EAGER=True,
    TSUNG_EXECUTABLE='/usr/bin/true')
class TestProfileRun(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.login(username='user', password='pass')

    def make_profile(self, name='testpr', url='http://example.com',
                     phase_duration=1, phase_rate=1):
        profile = models.Profile(
            name=name, url=url, phase_duration=phase_duration, phase_rate=1)
        profile.save()
        return profile

    def profile_run_url(self, id):
        return reverse('profile_run', kwargs={'id': id})

    def test_empty_profile(self):
        profile = self.make_profile()
        self.client.get(self.profile_run_url(profile.id))
        # TODO: Test that the right thing actually happened.


class TestProfileAddRequest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.login(username='user', password='pass')

    def make_profile(self, name='testpar', url='http://example.com',
                     phase_duration=1, phase_rate=1):
        profile = models.Profile(
            name=name, url=url, phase_duration=phase_duration, phase_rate=1)
        profile.save()
        return profile

    def profile_add_request_url(self, id):
        return reverse('profile_add_request', kwargs={'id': id})

    def profile_view_url(self, id):
        return reverse('profile_view', kwargs={'id': id})

    def assert_request_model(self, request, path, method, **fields):
        expected_values = {
            'http_auth': False,
            'path': path,
            'think_time': 1,
            'username': '',
            'password': '',
            'method': method,
            'content': '',
            'dyn_variable': '',
            'dyn_variable_attr': '',
            'dyn_variable_attr_value': '',
            'content_type': '',
            'order': 1,
        }
        expected_values.update(fields)
        actual_values = {
            'http_auth': request.http_auth,
            'path': request.path,
            'think_time': request.think_time,
            'username': request.username,
            'password': request.password,
            'method': request.method,
            'content': request.content,
            'dyn_variable': request.dyn_variable,
            'dyn_variable_attr': request.dyn_variable_attr,
            'dyn_variable_attr_value': request.dyn_variable_attr_value,
            'content_type': request.content_type,
            'order': request.order,
        }
        self.assertEqual(expected_values, actual_values)

    def test_add_simple(self):
        profile = self.make_profile()
        resp = self.client.post(self.profile_add_request_url(profile.id), {
            'path': '/',
            'think_time': '1',
            'method': 'GET',
        })
        self.assertRedirects(resp, self.profile_view_url(profile.id))
        [request] = profile.request_set.all()
        self.assert_request_model(request, path='/', method='GET')

    def test_add_dyn_variable(self):
        profile = self.make_profile()
        resp = self.client.post(self.profile_add_request_url(profile.id), {
            'path': '/',
            'think_time': '1',
            'method': 'GET',
            'dyn_variable': 'foo',
        })
        self.assertRedirects(resp, self.profile_view_url(profile.id))
        [request] = profile.request_set.all()
        self.assert_request_model(
            request, path='/', method='GET', dyn_variable='foo')

    def test_add_dyn_variable_attr(self):
        profile = self.make_profile()
        resp = self.client.post(self.profile_add_request_url(profile.id), {
            'path': '/',
            'think_time': '1',
            'method': 'GET',
            'dyn_variable': 'foo',
            'dyn_variable_attr': 'jsonpath',
            'dyn_variable_attr_value': 'foo.bar',
        })
        self.assertRedirects(resp, self.profile_view_url(profile.id))
        [request] = profile.request_set.all()
        self.assert_request_model(
            request, path='/', method='GET', dyn_variable='foo',
            dyn_variable_attr='jsonpath', dyn_variable_attr_value='foo.bar')
