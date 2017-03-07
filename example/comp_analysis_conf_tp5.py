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
            'binary': '/home/erahm/dev/atsy-test/firefox/firefox-bin',
            'parent_filter': lambda x: 'firefox-bin -content' not in x,
            'path_filter': lambda x: 'atsy-test/firefox' in x
        }
    },
}

# Talos TP5
TEST_SITES = [
    "http://localhost-1:8001/tp5/thesartorialist.blogspot.com/thesartorialist.blogspot.com/index.html",
    "http://localhost-2:8002/tp5/cakewrecks.blogspot.com/cakewrecks.blogspot.com/index.html",
    "http://localhost-3:8003/tp5/baidu.com/www.baidu.com/s@wd=mozilla.html",
    "http://localhost-4:8004/tp5/en.wikipedia.org/en.wikipedia.org/wiki/Rorschach_test.html",
    "http://localhost-5:8005/tp5/twitter.com/twitter.com/ICHCheezburger.html",
    "http://localhost-6:8006/tp5/msn.com/www.msn.com/index.html",
    "http://localhost-7:8007/tp5/yahoo.co.jp/www.yahoo.co.jp/index.html",
    "http://localhost-8:8008/tp5/amazon.com/www.amazon.com/Kindle-Wireless-Reader-Wifi-Graphite/dp/B002Y27P3M/507846.html",
    "http://localhost-9:8009/tp5/linkedin.com/www.linkedin.com/in/christopherblizzard@goback=.nppvan_%252Flemuelf.html",
    "http://localhost-10:8010/tp5/bing.com/www.bing.com/search@q=mozilla&go=&form=QBLH&qs=n&sk=&sc=8-0.html",
    "http://localhost-11:8011/tp5/icanhascheezburger.com/icanhascheezburger.com/index.html",
    "http://localhost-12:8012/tp5/yandex.ru/yandex.ru/yandsearch@text=mozilla&lr=21215.html",
    "http://localhost-13:8013/tp5/cgi.ebay.com/cgi.ebay.com/ALL-NEW-KINDLE-3-eBOOK-WIRELESS-READING-DEVICE-W-WIFI-/130496077314@pt=LH_DefaultDomain_0&hash=item1e622c1e02.html",
    "http://localhost-14:8014/tp5/163.com/www.163.com/index.html",
    "http://localhost-15:8015/tp5/mail.ru/mail.ru/index.html",
    "http://localhost-16:8016/tp5/bbc.co.uk/www.bbc.co.uk/news/index.html",
    "http://localhost-17:8017/tp5/store.apple.com/store.apple.com/us@mco=Nzc1MjMwNA.html",
    "http://localhost-18:8018/tp5/imdb.com/www.imdb.com/title/tt1099212/index.html",
    "http://localhost-19:8019/tp5/mozilla.com/www.mozilla.com/en-US/firefox/all-older.html",
    "http://localhost-20:8020/tp5/ask.com/www.ask.com/web@q=What%27s+the+difference+between+brown+and+white+eggs%253F&gc=1&qsrc=3045&o=0&l=dir.html",
    "http://localhost-21:8021/tp5/cnn.com/www.cnn.com/index.html",
    "http://localhost-22:8022/tp5/sohu.com/www.sohu.com/index.html",
    "http://localhost-23:8023/tp5/vkontakte.ru/vkontakte.ru/help.php@page=about.html",
    "http://localhost-24:8024/tp5/youku.com/www.youku.com/index.html",
    "http://localhost-25:8025/tp5/myparentswereawesome.tumblr.com/myparentswereawesome.tumblr.com/index.html",
    "http://localhost-26:8026/tp5/ifeng.com/ifeng.com/index.html",
    "http://localhost-27:8027/tp5/ameblo.jp/ameblo.jp/index.html",
    "http://localhost-28:8028/tp5/tudou.com/www.tudou.com/index.html",
    "http://localhost-29:8029/tp5/chemistry.about.com/chemistry.about.com/index.html",
    "http://localhost-30:8030/tp5/beatonna.livejournal.com/beatonna.livejournal.com/index.html",
]
