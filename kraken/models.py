import urlparse

from django.db import models
from lxml import etree


class Server(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    cores = models.IntegerField()


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

    class Meta:
        ordering = ['probability']


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

    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']


class Test(models.Model):
    profile = models.ForeignKey(Profile)
    test_time = models.DateTimeField(auto_now_add=True)

    running = models.BooleanField()

    task_id = models.CharField(max_length=255, default='')

    test_log = models.TextField(default="")
    stdout = models.TextField(default="")

    class Meta:
        ordering = ['-test_time']


def generate_config_xml(profile):
    # Build test doc structure
    root = etree.Element("tsung", loglevel="notice", version="1.0")
    clients = etree.SubElement(root, 'clients')
    servers = etree.SubElement(root, 'servers')
    load = etree.SubElement(root, 'load')
    options = etree.SubElement(root, 'options')
    sessions = etree.SubElement(root, 'sessions')

    # Setup clients - this really needs to be configurable for clusters etc.
    server_list = Server.objects.all()
    for server in server_list:
        clients.append(etree.Element('client',
            host=server.hostname,
            cpu=str(server.cores),
            maxusers="10000",
            weight="1"
        ))

    # Setup target server
    profile_server = urlparse.urlparse(profile.url)
    port = profile_server.port
    # but urlparse is retarded...
    if not port:
        if profile_server.scheme == 'http':
            port = 80
        elif profile_server.scheme == 'https':
            port = 443
        else:
            raise Exception('This is for testing webservers...')

    server = etree.SubElement(servers, 'server', host=profile_server.hostname,
        port=str(port), type="tcp")

    # Setup load phase (just one for now)
    arivalphase = etree.SubElement(load, 'arrivalphase', phase="1",
        duration=str(profile.phase_duration), unit="minute")

    arivalphase.append(etree.Element('users',
        interarrival="%0.2f" % (profile.phase_rate / 1000.0), unit="second"))

    # Setup user agents
    option = etree.SubElement(
        options, 'option', type="ts_http", name="user_agent")
    for agent in profile.useragent_set.all():
        agent_tag = etree.Element(
            'user_agent',
            probability=str(agent.probability)
        )
        agent_tag.text = agent.agent.agent  # Wow that was a shit idea...
        option.append(agent_tag)

    # Setup requests
    session = etree.SubElement(
        sessions, 'session', name=profile.name.lower(), probability='100',
        type='ts_http')
    first_request = True
    for request in profile.request_set.all():
        request_tag = etree.Element('request')

        if first_request:
            # Add the whole path
            url = urlparse.urljoin(profile.url, request.path)
            first_request = False
        else:
            url = request.path

        if request.dyn_variable:
            request_tag.append(
                etree.Element('dyn_variable', name=request.dyn_variable)
            )

        if request.method == 'POST':
            request_tag.append(etree.Element(
                'http', url=url, version='1.1', method='POST',
                content_type=request.content_type, contents=request.content))
        else:
            request_tag.append(etree.Element(
                'http', url=url, version='1.1', method=request.method))

        if request.think_time:
            think_tag = etree.Element(
                'thinktime', random='true', value=str(request.think_time))
            session.append(think_tag)

        session.append(request_tag)

    return etree.tostring(
        root, pretty_print=True,
        doctype='<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">')
