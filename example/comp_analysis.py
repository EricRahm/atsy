#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import os

import mozinfo
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from atsy.stats import ProcessStats
from atsy.multitab import (
    FirefoxMultiTabTest, ManualMultiTabTest, MultiTabTest)


def test_browser(browser, stats, binary, urls,
                 per_tab_pause, settle_wait_time,
                 proxy, process_count):

    test_options = {
        'per_tab_pause': per_tab_pause,
        'settle_wait_time': settle_wait_time
    }

    if browser == 'Chrome':
        options = webdriver.chrome.options.Options()
        options.binary_location = binary
        caps = options.to_capabilities()

        if proxy:
            webdriver_proxy = webdriver.Proxy()
            webdriver_proxy.http_proxy = proxy
            webdriver_proxy.add_to_capabilities(caps)

        driver = webdriver.Chrome(desired_capabilities=caps)

        test = MultiTabTest(driver, stats, **test_options)
        test.open_urls(urls)

        driver.quit()
    elif browser == 'Firefox':
        for count in process_count:
            print "FIREFOX WITH %d CONTENT PROCESSES" % count
            test = FirefoxMultiTabTest(binary, stats, proxy=proxy, process_count=count, **test_options)
            test.open_urls(urls)
    elif browser in ('Safari', 'IE'):
        # Currently this is a manual test, sorry.
        manual_test = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'comp_analysis_manual_test.htm'))
        test = ManualMultiTabTest(binary, stats, **test_options)
        prefix = 'file://' if browser == 'IE' else ''
        test.open_urls([prefix + manual_test])
    elif browser == 'Edge':
        # Currently this is even more manual than IE and Safari. Edge won't
        # let us provide a path to launch.
        print "Open up explorer, find 'atsy/example/comp_analysis_manual_test.htm'"
        print "Right-click, 'Open with' -> 'Microsoft Edge'"
        print "Run the test, press enter when it's done."
        import sys
        sys.stdin.read(1)
        stats.print_stats()
    else:
        raise Exception("Unhandled browser: %s" % browser)


def test_browsers(browsers, setup, test_sites,
                  per_tab_pause, settle_wait_time, proxy=None,
                  process_count=(2,4,8)):
    for browser in browsers:
        config = setup[mozinfo.os][browser]
        stats = ProcessStats(config['path_filter'], config['parent_filter'])
        binary = config['binary']

        test_browser(browser, stats, binary, test_sites,
                     per_tab_pause, settle_wait_time, proxy,
                     process_count)


def main():
    # Default path to the config file containing the SETUP and TEST_SITES vars.
    default_config = os.path.join(
            os.path.dirname(__file__), 'comp_analysis_conf_simple.py')

    # Default browsers to test.
    default_browsers = [ 'Chrome', 'Firefox' ]

    if mozinfo.os == 'win':
        default_browsers.append('IE')
        if mozinfo.version.startswith('10'):
            default_browsers.append('Edge')
    elif mozinfo.os == 'mac':
        default_browsers.append('Safari')

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', action='append', dest='browsers',
                        default=[],
                        help='Adds a browser to the list of browsers to test.')
    parser.add_argument('-c', action='store', dest='conf_file',
                        default=default_config,
                        help='A python file containing the test configuration.')
    parser.add_argument('-q', action='store_true', default=False, dest='quick',
                        help='Perform a quick test of 3 sites, minimal pauses.')
    parser.add_argument('--per_tab_pause', action='store', dest='per_tab_pause',
                        default='10', type=float,
                        help='Amount of time in seconds to stay on a tab.')
    parser.add_argument('--settle_wait_time', action='store', dest='settle_wait_time',
                        default='60', type=float,
                        help='Amount of time in seconds to wait before measuring memory.')
    parser.add_argument('--proxy', action='store', dest='proxy', default=None,
                        help='HTTP proxy to use. e.g "localhost:3128". Only works with Chrome and Firefox currently.')
    parser.add_argument('--content-processes', action='append', dest='process_count',
                        default=[], type=float,
                        help='The number of content processes to use for Firefox.')

    cmdline = parser.parse_args()
    if not cmdline.browsers:
        cmdline.browsers = default_browsers

    if cmdline.quick:
        cmdline.per_tab_pause = 1
        cmdline.settle_wait_time = 0

    if not cmdline.process_count:
        cmdline.process_count = (2, 4, 8)

    # This loads |SETUP| and |TEST_SITES|.
    out = {}
    execfile(cmdline.conf_file, {}, out)
    TEST_SITES = out['TEST_SITES']
    SETUP = out['SETUP']

    if cmdline.quick and len(TEST_SITES) > 3:
        TEST_SITES = TEST_SITES[:3]

    test_browsers(cmdline.browsers, SETUP, TEST_SITES,
                  cmdline.per_tab_pause, cmdline.settle_wait_time,
                  cmdline.proxy, cmdline.process_count)


if __name__ == '__main__':
    main()
