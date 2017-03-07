# This file provides a configuration for running the atsy tests.
#
# Format:
# SETUP = {
#     '<os_name>': {
#         '<browser_name>': {
#             'binary': Path to the browser executable,
#             'parent_filter': lambda function used to differentiate the
#                              parent process from the content processes
#
#                              The full command line is passed to it,
#             'path_filter': lambda function used to determine if the given
#                            process path is related to the browser.
#         },
#     },
# }
#
# TEST_SITES = [
#     <list of URLs to run through>
# ]

SETUP = {
    'mac': {
        'Firefox': {
            'binary': '/Users/ericrahm/dev/mozilla-central/obj-x86_64-apple-darwin14.5.0-release/dist/Nightly.app/Contents/MacOS/firefox',
            'parent_filter': lambda x: 'firefox' in x,
            'path_filter': lambda x: '/Nightly.app/' in x
        },
        'Chrome': {
            'binary': '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
            'parent_filter': lambda x: 'Google Chrome Helper' not in x,
            'path_filter': lambda x: 'Google Chrome Canary.app' in x
        },
        'Safari': {
            'binary': '/Applications/Safari.app/Contents/MacOS/Safari',
            # We'll treat anything that's not 'WebContent' as a parent
            'parent_filter': lambda x: 'WebContent' not in x,
            # Safari uses a fair amount of system processes, this probably isn't
            # all of them
            'path_filter': lambda x: any(a in x for a in ('ComponentHelper', 'SandboxHelper', 'Safari', 'WebKit'))
        }
    },
    'win': {
        'Chrome': {
            'binary': r'C:\Users\moz21268\AppData\Local\Google\Chrome SxS\Application\chrome.exe',
            'parent_filter': lambda x: '/prefetch' not in x,
            'path_filter': lambda x: 'Chrome SxS' in x
        },
        'Firefox': {
            'binary': r'c:\dev\comp_analysis\2016-01-26-03-02-44-mozilla-central-firefox-47\core\firefox.exe',
            'parent_filter': lambda x: 'firefox.exe' in x,
            'path_filter': lambda x: 'mozilla-central' in x
        },
        'IE': {
            'binary': r'C:\Program Files\Internet Explorer\iexplore.exe',
            'parent_filter': lambda x: 'iexplore.exe' in x,
            'path_filter': lambda x: 'Internet Explorer' in x
        },
        'Edge': {
            'binary': None,
            'parent_filter': lambda x: 'microsoftedgecp.exe' not in x,
            'path_filter': lambda x: 'MicrosoftEdge' in x
        }
    },
    'linux': {
        'Chrome': {
            'binary': '/usr/bin/google-chrome-unstable',
            'parent_filter': lambda x: 'chrome --type' not in x,
            'path_filter': lambda x: 'chrome-unstable' in x
        },
        'Firefox': {
            'binary': 'firefox/firefox-bin',
            'parent_filter': lambda x: 'firefox-bin' in x,
            'path_filter': lambda x: 'atsy-test/firefox' in x
        }
    },
}

# Example test sites.
TEST_SITES = [
    "https://www.google.com/#q=red+panda",
    "https://yahoo.com",
    "http://cnn.com",
    "https://www.youtube.com/watch?v=DSehQsYU9h4",
    "https://www.linkedin.com/company/mozilla-corporation"
]
