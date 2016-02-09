# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from marionette.runtests import MarionetteTestRunner
import mozinfo
from mozlog.structured import commandline
import mozprofile

import os
import shutil
import subprocess
import sys
import time

# Maximum number of tabs to open
MAX_TABS = 30

# Default amount of seconds to wait in between opening tabs
PER_TAB_PAUSE = 10

# Default amount of time to wait after loading all tabs.
SETTLE_WAIT_TIME = 60

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseMultiTabTest:

    def __init__(self, stats,
                 per_tab_pause=PER_TAB_PAUSE,
                 settle_wait_time=SETTLE_WAIT_TIME):
        self.per_tab_pause = per_tab_pause
        self.settle_wait_time = settle_wait_time
        self.stats = stats

    def open_urls(self, urls):
        raise NotImplementedError()


class ManualMultiTabTest(BaseMultiTabTest):

    def __init__(self, binary, stats, per_tab_pause=PER_TAB_PAUSE,
                 settle_wait_time=SETTLE_WAIT_TIME):
        BaseMultiTabTest.__init__(self, stats, per_tab_pause, settle_wait_time)
        self.binary = binary

    def open_urls(self, urls):
        if len(urls) != 1:
            raise Exception("The manual test requires exactly one URL.")

        # Safari prefixes all command-line urls w/ 'file://', escapes the '?'
        # in the query string. So lets just not do that.
        # manual_test_file = \
        #    "%s?per_tab_pause=%d&settle_wait_time=%d" % \
        #        (urls[0], self.per_tab_pause, self.settle_wait_time)
        manual_test_file = urls[0]

        p = subprocess.Popen([self.binary, manual_test_file], close_fds=True)

        print "Do what the page says, then press enter when it's done loading the tests."
        sys.stdin.read(1)

        self.stats.print_stats(verbose=True)
        p.kill()


class FirefoxMultiTabTest(BaseMultiTabTest):
    """
    For Firefox we can't use webdriver with e10s enabled, so instead we use
    marionette directly. See also the test_memory_usage.py file for the
    actual test implementation.

    This is based on the areweslimyet MarionetteTest.
    """

    def __init__(self, binary, stats, process_count=1,
                 per_tab_pause=PER_TAB_PAUSE,
                 settle_wait_time=SETTLE_WAIT_TIME,
                 proxy=None):
        BaseMultiTabTest.__init__(
            self, stats, per_tab_pause, settle_wait_time)

        self.binary = binary
        self.process_count = process_count
        if proxy:
            proxy_details = proxy.split(':')
            self.proxy = proxy_details[0]
            if len(proxy_details) > 1:
                self.proxy_port = int(proxy_details[1])
            else:
                self.proxy_port = 3128
        else:
            self.proxy = None

    def open_urls(self, urls, marionette_port=24242):
        testvars = {
            'perTabPause': self.per_tab_pause,
            'settleWaitTime': self.settle_wait_time,
            'entities': len(urls),
            'urls': urls,
            'stats': self.stats,
        }

        e10s = self.process_count > 0

        prefs = {

            # Don't open the first-run dialog, it loads a video
            'startup.homepage_welcome_url': '',
            'startup.homepage_override_url': '',
            'browser.newtab.url': 'about:blank',

            # make sure e10s is enabled
            "browser.tabs.remote.autostart": e10s,
            "browser.tabs.remote.autostart.1": e10s,
            "browser.tabs.remote.autostart.2": e10s,
            "browser.tabs.remote.autostart.3": e10s,
            "browser.tabs.remote.autostart.4": e10s,
            "browser.tabs.remote.autostart.5": e10s,
            "browser.tabs.remote.autostart.6": e10s,
            "dom.ipc.processCount": self.process_count,

            # prevent "You're using e10s!" dialog from showing up
            "browser.displayedE10SNotice": 1000,

            # override image expiration in hopes of getting less volatile
            # numbers
            "image.mem.surfacecache.min_expiration_ms": 10000,

            # Specify a communications port
            "marionette.defaultPrefs.port": marionette_port,
        }

        if self.proxy:
            # disable network access
            prefs.update({
                "network.proxy.socks": self.proxy,
                "network.proxy.socks_port": self.proxy_port,
                "network.proxy.socks_remote_dns": True,
                "network.proxy.type": 1,  # Socks
            })

        profile = mozprofile.FirefoxProfile(preferences=prefs)

        # TODO(ER): Figure out how to turn on debug level info again
        #commandline.formatter_option_defaults['level'] = 'debug'

        logger = commandline.setup_logging("MarionetteTest", {})
        runner = MarionetteTestRunner(
            binary=self.binary,
            profile=profile,
            logger=logger,
            startup_timeout=60,
            address="localhost:%d" % marionette_port)

        # Add our testvars
        runner.testvars.update(testvars)

        test_path = os.path.join(MODULE_DIR, "test_memory_usage.py")
        try:
            print "Marionette - running test"
            runner.run_tests([test_path])
            failures = runner.failed
        except Exception, e:
            print e
            pass

        try:
            runner.cleanup()
        except Exception, e:
            print "Failed to cleanup"

        # cleanup the profile dir if not already cleaned up
        if os.path.exists(profile.profile):
            shutil.rmtree(profile.profile)


class MultiTabTest(BaseMultiTabTest):
    """
    Many attempts have been made to make this cross-browser. Unfortunately each browser
    and each OS has its own webdriver deficiencies. The current version seems to work
    on Chrome.

    Below are a few of the issues as far as I can recall, there are probably
    more.

    Issues with IE:
      - It doesn't handle data URLs for HTML.
      - Ctrl-Shift-Clicking the anchor doesn't open a new tab, it just navigates
        the current tab.
      - It can load, but not interact with a file:// URL.
      - Opening a new tab causes |driver.window_handles| to become empty.

    Issues with Edge:
      - AFAICT their webdriver does not implement the functionality that we
        need.
      - It needs Windows 10, I downloaded a VM but didn't get around to testing
        given issue #1.

    Issues with Firefox:
      - Using webdriver w/ e10s enabled is broken.
      - Sending ActionChains does not work.

    Issues with Chrome:
      - When selecting a new tab the visual focus is not changed. We work around
        that by loading a generated page of URLs, Ctrl-Shift-Clicking each
        anchor tag, the new page is visually loaded, and then we advance to the
        next tag.

    Issues with Safari:
      - Safari's webdriver is broken and cannnot be installed in the most
        recent version of Safari.

    Issues with Opera:
      - Unknown, I chose not to try Opera given it uses blink and we're already
        testing Chrome.
    """

    def __init__(self, driver, stats,
                 per_tab_pause=PER_TAB_PAUSE,
                 settle_wait_time=SETTLE_WAIT_TIME):
        BaseMultiTabTest.__init__(self, stats, per_tab_pause, settle_wait_time)
        self.driver = driver
        self.tabs = driver.window_handles
        self.idx = len(self.tabs) - 1

        # One of the browsers got grumpy if we didn't load a fake page.
        # This probably isn't necessary anymore, but might help in a desparate
        # situation.
        # self.driver.get('data:text/html,<html><body>Hello!</body></html>')

    def open_tab(self, url):
        """
        Opens a new tab and switches focus to it.

        NB: Currently not used because send_keys on the driver doesn't work on OSX
            for Chrome (at least, might be others).
        """
        orig_handles = self.driver.window_handles

        if mozinfo.os == "mac":
            self.driver.find_element_by_tag_name(
                'body').send_keys(Keys.COMMAND + "t")
        else:
            self.driver.find_element_by_tag_name(
                'body').send_keys(Keys.CONTROL + "t")

        time.sleep(0.25)

        new_handles = set(self.driver.window_handles) - orig_handles
        new_handle = list(new_handles)[0]
        self.driver.switch_to_window(new_handle)
        self.driver.get(url)

        # On Fx at least the handle can change after you load content.
        new_handles = set(self.driver.window_handles) - orig_handles
        new_handle = list(new_handles)[0]

        self.tabs.append(new_handle)

    def open_urls_fx(self, urls, per_tab_pause=PER_TAB_PAUSE):
        """
        This seemed to work for non-e10s Firefox at one point.
        """
        for url in urls:
            self.open_tab(url)
            time.sleep(per_tab_pause)

        time.sleep(SETTLE_WAIT_TIME)
        self.stats.print_stats()

    def open_urls(self, urls, tab_limit=MAX_TABS):
        """
        This works at least on Chrome across platforms.
        """
        # First setup a document with the target URLs.
        link_doc = 'data:text/html,'
        link_doc += '<html><head><title>Links!</title></head><body>'
        id = 0
        for url in urls:
            link_doc += '<a id="%d" href="%s">%d: %s</a><br>' % (
                id, url, id, url)
            id += 1

        link_doc += '</body><html>'
        self.driver.get(link_doc)

        # Now open each document in a new tab by ctrl+shift clicking the
        # anchor.
        for tag in self.driver.find_elements_by_tag_name("a"):
            action = ActionChains(self.driver)

            if mozinfo.os == "mac":
                ctrl_key = Keys.COMMAND
            else:
                ctrl_key = Keys.CONTROL

            action.key_down(ctrl_key).key_down(Keys.SHIFT).click(
                tag).key_up(Keys.SHIFT).key_up(ctrl_key).perform()
            time.sleep(self.per_tab_pause)

        time.sleep(self.settle_wait_time)
        self.stats.print_stats()
