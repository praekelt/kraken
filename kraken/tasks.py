from celery import task

import os
import sys
import subprocess
import time

from kraken import tsung

@task()
def run_test(test, test_xml):
    # Use subprocess to execute a test, update the db with results
    profile = test.profile
    now = time.strftime("%Y%m%d-%H%M")

    fname = '%s-%s' % (profile.name.lower(), now)

    testfile = '/tmp/%s.xml' % fname
    testlog = '/tmp/%s/' % fname

    os.makedirs(testlog)

    testfh = open(testfile, 'wt')
    testfh.write(test_xml)
    testfh.close()

    args = ['/usr/bin/tsung', '-f', testfile, '-l', testlog, 'start']

    print args
    
    # Execute tsung
    test_runner = subprocess.Popen(args,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env={"HOME":os.getcwd()})
    test_runner.wait()

    test.stdout = test_runner.stdout.read()

    if test_runner.returncode == 0:
        # Why must tsung do crazy things to the path I give it
        log_dir = os.listdir(testlog)[0]
        real_log = os.path.join(testlog, log_dir, fname)

        json_data = tsung.parse_stats(real_log)

        test.test_log = json_data

        test.running = False

    test.save()
