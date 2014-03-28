from django.test import TestCase

from kraken import models


class TestGenerateConfig(TestCase):
    def make_profile(self, name='testgc', url='http://example.com',
                     phase_duration=1, phase_rate=1):
        profile = models.Profile(
            name=name, url=url, phase_duration=phase_duration, phase_rate=1)
        profile.save()
        return profile

    def add_request(self, profile, think_time=1, **kw):
        request = models.Request(profile=profile, think_time=think_time, **kw)
        request.save()
        return request

    def assertXML(self, xml, lines):
        self.assertEqual(xml, '\n'.join(lines) + '\n')

    def test_empty_profile(self):
        profile = self.make_profile()
        xml = models.generate_config_xml(profile)
        self.assertXML(xml, [
            '<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">',
            '<tsung loglevel="notice" version="1.0">',
            '  <clients/>',
            '  <servers>',
            '    <server host="example.com" port="80" type="tcp"/>',
            '  </servers>',
            '  <load>',
            '    <arrivalphase duration="1" phase="1" unit="minute">',
            '      <users interarrival="0.00" unit="second"/>',
            '    </arrivalphase>',
            '  </load>',
            '  <options>',
            '    <option name="user_agent" type="ts_http"/>',
            '  </options>',
            '  <sessions>',
            '    <session name="testgc" probability="100" type="ts_http"/>',
            '  </sessions>',
            '</tsung>',
        ])

    def test_simple_request(self):
        profile = self.make_profile()
        self.add_request(profile)
        xml = models.generate_config_xml(profile)
        self.assertXML(xml, [
            '<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">',
            '<tsung loglevel="notice" version="1.0">',
            '  <clients/>',
            '  <servers>',
            '    <server host="example.com" port="80" type="tcp"/>',
            '  </servers>',
            '  <load>',
            '    <arrivalphase duration="1" phase="1" unit="minute">',
            '      <users interarrival="0.00" unit="second"/>',
            '    </arrivalphase>',
            '  </load>',
            '  <options>',
            '    <option name="user_agent" type="ts_http"/>',
            '  </options>',
            '  <sessions>',
            '    <session name="testgc" probability="100" type="ts_http">',
            '      <thinktime random="true" value="1"/>',
            '      <request>',
            '        <http method="" url="http://example.com" version="1.1"/>',
            '      </request>',
            '    </session>',
            '  </sessions>',
            '</tsung>',
        ])

    def test_request_dyn_variable(self):
        profile = self.make_profile()
        self.add_request(profile, dyn_variable='foo')
        xml = models.generate_config_xml(profile)
        self.assertXML(xml, [
            '<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">',
            '<tsung loglevel="notice" version="1.0">',
            '  <clients/>',
            '  <servers>',
            '    <server host="example.com" port="80" type="tcp"/>',
            '  </servers>',
            '  <load>',
            '    <arrivalphase duration="1" phase="1" unit="minute">',
            '      <users interarrival="0.00" unit="second"/>',
            '    </arrivalphase>',
            '  </load>',
            '  <options>',
            '    <option name="user_agent" type="ts_http"/>',
            '  </options>',
            '  <sessions>',
            '    <session name="testgc" probability="100" type="ts_http">',
            '      <thinktime random="true" value="1"/>',
            '      <request>',
            '        <dyn_variable name="foo"/>',
            '        <http method="" url="http://example.com" version="1.1"/>',
            '      </request>',
            '    </session>',
            '  </sessions>',
            '</tsung>',
        ])

    def test_request_dyn_variable_jsonpath(self):
        profile = self.make_profile()
        self.add_request(
            profile, dyn_variable='foo', dyn_variable_attr='jsonpath',
            dyn_variable_attr_value="foo.bar")
        xml = models.generate_config_xml(profile)
        self.assertXML(xml, [
            '<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">',
            '<tsung loglevel="notice" version="1.0">',
            '  <clients/>',
            '  <servers>',
            '    <server host="example.com" port="80" type="tcp"/>',
            '  </servers>',
            '  <load>',
            '    <arrivalphase duration="1" phase="1" unit="minute">',
            '      <users interarrival="0.00" unit="second"/>',
            '    </arrivalphase>',
            '  </load>',
            '  <options>',
            '    <option name="user_agent" type="ts_http"/>',
            '  </options>',
            '  <sessions>',
            '    <session name="testgc" probability="100" type="ts_http">',
            '      <thinktime random="true" value="1"/>',
            '      <request>',
            '        <dyn_variable name="foo" jsonpath="foo.bar"/>',
            '        <http method="" url="http://example.com" version="1.1"/>',
            '      </request>',
            '    </session>',
            '  </sessions>',
            '</tsung>',
        ])

    def test_request_post(self):
        profile = self.make_profile()
        self.add_request(
            profile, method='POST', content_type='application/json',
            content='{}')
        xml = models.generate_config_xml(profile)
        self.assertXML(xml, [
            '<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">',
            '<tsung loglevel="notice" version="1.0">',
            '  <clients/>',
            '  <servers>',
            '    <server host="example.com" port="80" type="tcp"/>',
            '  </servers>',
            '  <load>',
            '    <arrivalphase duration="1" phase="1" unit="minute">',
            '      <users interarrival="0.00" unit="second"/>',
            '    </arrivalphase>',
            '  </load>',
            '  <options>',
            '    <option name="user_agent" type="ts_http"/>',
            '  </options>',
            '  <sessions>',
            '    <session name="testgc" probability="100" type="ts_http">',
            '      <thinktime random="true" value="1"/>',
            '      <request>',
            ('        <http method="POST" url="http://example.com"'
             ' version="1.1" content_type="application/json" contents="{}"/>'),
            '      </request>',
            '    </session>',
            '  </sessions>',
            '</tsung>',
        ])

    def test_request_put(self):
        profile = self.make_profile()
        self.add_request(
            profile, path='/foo', method='PUT',
            content_type='application/json', content='{}')
        xml = models.generate_config_xml(profile)
        self.assertXML(xml, [
            '<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">',
            '<tsung loglevel="notice" version="1.0">',
            '  <clients/>',
            '  <servers>',
            '    <server host="example.com" port="80" type="tcp"/>',
            '  </servers>',
            '  <load>',
            '    <arrivalphase duration="1" phase="1" unit="minute">',
            '      <users interarrival="0.00" unit="second"/>',
            '    </arrivalphase>',
            '  </load>',
            '  <options>',
            '    <option name="user_agent" type="ts_http"/>',
            '  </options>',
            '  <sessions>',
            '    <session name="testgc" probability="100" type="ts_http">',
            '      <thinktime random="true" value="1"/>',
            '      <request>',
            ('        <http method="PUT" url="http://example.com/foo"'
             ' version="1.1" content_type="application/json" contents="{}"/>'),
            '      </request>',
            '    </session>',
            '  </sessions>',
            '</tsung>',
        ])

    def test_request_auth(self):
        profile = self.make_profile()
        self.add_request(
            profile, http_auth=True, username='user', password='pass')
        xml = models.generate_config_xml(profile)
        self.assertXML(xml, [
            '<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">',
            '<tsung loglevel="notice" version="1.0">',
            '  <clients/>',
            '  <servers>',
            '    <server host="example.com" port="80" type="tcp"/>',
            '  </servers>',
            '  <load>',
            '    <arrivalphase duration="1" phase="1" unit="minute">',
            '      <users interarrival="0.00" unit="second"/>',
            '    </arrivalphase>',
            '  </load>',
            '  <options>',
            '    <option name="user_agent" type="ts_http"/>',
            '  </options>',
            '  <sessions>',
            '    <session name="testgc" probability="100" type="ts_http">',
            '      <thinktime random="true" value="1"/>',
            '      <request>',
            '        <http method="" url="http://example.com" version="1.1">',
            '          <www_authenticate passwd="pass" userid="user"/>',
            '        </http>',
            '      </request>',
            '    </session>',
            '  </sessions>',
            '</tsung>',
        ])
