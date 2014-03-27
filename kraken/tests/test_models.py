from django.test import TestCase

from kraken import models


class TestGenerateConfig(TestCase):
    def make_profile(self, name='testprofile', url='http://example.com',
                     phase_duration=1, phase_rate=1):
        return models.Profile(
            name=name, url=url, phase_duration=phase_duration, phase_rate=1)

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
            ('    <session name="testprofile" probability="100" '
             'type="ts_http"/>'),
            '  </sessions>',
            '</tsung>',
        ])
