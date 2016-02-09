# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
import os
import sys

from marionette import MarionetteTestCase
from marionette_driver import Actions
import mozlog.structured
from marionette_driver.keys import Keys

# Default amount of tabs to have open at one time.
MAX_TABS = 30

# Default amount of seconds to wait in between opening tabs
PER_TAB_PAUSE = 10

# Default amount of seconds to wait for things to be settled down
SETTLE_WAIT_TIME = 60


class TestMemoryUsage(MarionetteTestCase):
    """
    Marionette test case used to open up tabs and measure memory.
    """

    def setUp(self):
        MarionetteTestCase.setUp(self)

        self.marionette.set_context('chrome')
        self.logger = mozlog.structured.structuredlog.get_default_logger()

        self.urls = self.testvars["urls"]
        self.pages_to_load = self.testvars.get("entities", len(self.urls))
        self.perTabPause = self.testvars.get("perTabPause", PER_TAB_PAUSE)
        self.settleWaitTime = self.testvars.get(
            "settleWaitTime", SETTLE_WAIT_TIME)
        self.maxTabs = self.testvars.get("maxTabs", MAX_TABS)
        self.stats = self.testvars.get("stats")

        # self.reset_state()

    def tearDown(self):
        self.logger.debug("tearing down!")
        MarionetteTestCase.tearDown(self)
        self.logger.debug("done tearing down!")

    def reset_state(self):
        self.pages_loaded = 0
        self.tabs = self.marionette.window_handles
        self.marionette.switch_to_window(self.tabs[0])

    def open_and_focus(self):
        """
        Opens the next URL in the list and focuses on the tab it is opened in.

        A new tab will be opened if |_maxTabs| has not been exceeded, otherwise
        the URL will be loaded in the next tab.
        """
        page_to_load = self.urls[self.pages_loaded % len(self.urls)]
        tabs_loaded = len(self.tabs)
        is_new_tab = False

        if tabs_loaded < self.maxTabs and tabs_loaded <= self.pages_loaded:
            full_tab_list = self.marionette.window_handles

            # Trigger opening a new tab by finding the new tab button and
            # clicking it
            newtab_button = (self.marionette.find_element('id', 'tabbrowser-tabs')
                                            .find_element('anon attribute',
                                                          {'anonid': 'tabs-newtab-button'}))
            newtab_button.click()

            self.wait_for_condition(lambda mn: len(
                mn.window_handles) == tabs_loaded + 1)

            # NB: The tab list isn't sorted, so we do a set diff to determine
            #     which is the new tab
            new_tab_list = self.marionette.window_handles
            new_tabs = list(set(new_tab_list) - set(full_tab_list))

            self.tabs.append(new_tabs[0])
            tabs_loaded += 1

            is_new_tab = True

        tab_idx = self.pages_loaded % self.maxTabs

        tab = self.tabs[tab_idx]

        # Tell marionette which tab we're on
        # NB: As a work-around for an e10s marionette bug, only select the tab
        #     if we're really switching tabs.
        if tabs_loaded > 1:
            self.logger.debug("switching to tab")
            self.marionette.switch_to_window(tab)
            self.logger.debug("switched to tab")

        with self.marionette.using_context('content'):
            self.logger.info("loading %s" % page_to_load)
            self.marionette.navigate(page_to_load)
            self.logger.debug("loaded!")

        # On e10s the tab handle can change after actually loading content
        if is_new_tab:
            # First build a set up w/o the current tab
            old_tabs = set(self.tabs)
            old_tabs.remove(tab)
            # Perform a set diff to get the (possibly) new handle
            [new_tab] = set(self.marionette.window_handles) - old_tabs
            # Update the tab list at the current index to preserve the tab
            # ordering
            self.tabs[tab_idx] = new_tab

        # give the page time to settle
        time.sleep(self.perTabPause)

        self.pages_loaded += 1

    def signal_user_active(self):
        """Signal to the browser that the user is active.

        Normally when being driven by marionette the browser thinks the
        user is inactive the whole time because user activity is
        detected by looking at key and mouse events.

        This would be a problem for this test because user inactivity is
        used to schedule some GCs (in particular shrinking GCs), so it
        would make this unrepresentative of real use.

        Instead we manually cause some inconsequential activity (a press
        and release of the shift key) to make the browser think the user
        is active.  Then when we sleep to allow things to settle the
        browser will see the user as becoming inactive and trigger
        appropriate GCs, as would have happened in real use.
        """
        action = Actions(self.marionette)
        action.key_down(Keys.SHIFT)
        action.key_up(Keys.SHIFT)
        action.perform()

    def test_open_tabs(self):
        """
        Opens tabs, measures memory.
        """
        self.logger.info("test_open_tabs")

        # This gives Firefox time to get into an OK state.
        time.sleep(10)

        self.reset_state()

        for x in range(self.pages_to_load):
            self.open_and_focus()
            self.signal_user_active()

        time.sleep(self.settleWaitTime)

        self.stats.print_stats()
