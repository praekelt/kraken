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

    def make_profile(self, name='testprofile', url='http://example.com',
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
