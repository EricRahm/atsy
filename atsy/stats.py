# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import mozinfo
import psutil
import StringIO
from subprocess import Popen, PIPE


class ProcessNotFoundException(Exception):
    """
    Indicates the desired process tree was not found.
    """
    pass


class ProcessStats:
    """
    Wrapper for psutil that provides a cross-platform way of tallying up
    the RSS of a parent process and the USS of its children.
    """

    def __init__(self, path_filter, parent_filter):
        self.path_filter = path_filter
        self.parent_filter = parent_filter

    def get_cmdline(self, proc):
        if mozinfo.os == "win":
            # The psutil.cmdline() implementation on Windows is pretty busted,
            # in particular it doesn't handle getting the command line of a
            # 64-bit process from a 32-bit python process very well.
            #
            # Instead we just shell out the WMIC command which works rather
            # well.
            cmd = "WMIC path win32_process where handle='%d' get Commandline" % (
                proc.pid)
            process = Popen(cmd.split(), stdout=PIPE)
            (output, err) = process.communicate()
            process.wait()

            # The output of WMIC is something like:
            #   Commandline
            #
            #
            #   path/to/exe --args etc

            buf = StringIO.StringIO(output)
            buf.readline()  # header
            for line in buf:
                if line.strip():
                    return line.strip()

            # If all else fails, just return the executable path.
            return p.exe()
        else:
            return " ".join(proc.cmdline())

    def print_stats(self, verbose=False):
        """
        Prints out stats for each matched process and a sum of the RSS of the
        parent process and the USS of its children.

        :param verbose: Set true to see the full command-line. This is useful
         when deciding on a parent filter.
        """
        def wrapped_path_filter(x):
            try:
                return self.path_filter(x.exe())
            except (psutil.AccessDenied, psutil.ZombieProcess):
                return False

        # On Windows psutil reports the RSS as wset.
        if mozinfo.os == "win":
            def rss_uss(info):
                return (info.wset, info.uss)
        else:
            def rss_uss(info):
                return (info.rss, info.uss)

        parent_rss = 0
        children_uss = 0

        for p in filter(wrapped_path_filter, psutil.process_iter()):
            (rss, uss) = rss_uss(p.memory_info_ex())
            cmdline = self.get_cmdline(p)

            exe = cmdline if verbose else p.exe()
            print "[%d] - %s\n  RSS - %d\n  USS - %d" % (p.pid, exe, rss, uss)

            if self.parent_filter(cmdline):
                parent_rss += rss
            else:
                children_uss += uss

        if not parent_rss:
            if not children_uss:
                raise ProcessNotFoundException(
                    "No processes matched the path filter")
            else:
                raise ProcessNotFoundException(
                    "No process matched the parent filter")

        print "\nTotal: {:,} bytes\n".format(parent_rss + children_uss)

if __name__ == "__main__":
    # Simple adhoc test, not meant to really be used.

    if mozinfo.os == "win":
        # Test firefox
        stats = ProcessStats(lambda x: "Nightly" in x,
                             lambda x: "firefox.exe" in x)
        stats.print_stats()

        # Test chrome
        stats = ProcessStats(lambda x: "Chrome SxS" in x,
                             lambda x: "/prefetch" not in x)
        stats.print_stats()
    else:
        raise Exception("Implement adhoc test for other platforms")
