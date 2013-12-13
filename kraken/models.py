from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255)

    phase_duration = models.IntegerField()
    phase_rate = models.IntegerField()

class UserAgents(models.Model):
    name = models.CharField(max_length=255, unique=True)
    agent = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__().encode('utf-8', 'replace')

class UserAgent(models.Model):
    profile = models.ForeignKey(Profile)
    agent = models.ForeignKey(UserAgents)
    probability = models.IntegerField()

    def __unicode__(self):
        return self.agent.name

    def __str__(self):
        return self.__unicode__().encode('utf-8', 'replace')

class Request(models.Model):
    profile = models.ForeignKey(Profile)

    http_auth = models.BooleanField()

    path = models.CharField(max_length=255)

    think_time = models.IntegerField()

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    method = models.CharField(max_length=5)
    content = models.CharField(max_length=255)

    dyn_variable = models.CharField(max_length=255)

    content_type = models.CharField(max_length=255)

class Test(models.Model):
    profile = models.ForeignKey(Profile)
    test_time = models.DateTimeField(auto_now_add=True)

    running = models.BooleanField()

    task_id = models.CharField(max_length=255, default='')
