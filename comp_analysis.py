#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import mozinfo

from atsy.stats import ProcessStats
from atsy.multitab import (FirefoxMultiTabTest, MultiTabTest)


# Talos TP5
TEST_SITES = [
  "http://localhost:8001/tp5/thesartorialist.blogspot.com/thesartorialist.blogspot.com/index.html",
  "http://localhost:8002/tp5/cakewrecks.blogspot.com/cakewrecks.blogspot.com/index.html",
  "http://localhost:8003/tp5/baidu.com/www.baidu.com/s@wd=mozilla.html",
  "http://localhost:8004/tp5/en.wikipedia.org/en.wikipedia.org/wiki/Rorschach_test.html",
  "http://localhost:8005/tp5/twitter.com/twitter.com/ICHCheezburger.html",
  "http://localhost:8006/tp5/msn.com/www.msn.com/index.html",
  "http://localhost:8007/tp5/yahoo.co.jp/www.yahoo.co.jp/index.html",
  "http://localhost:8008/tp5/amazon.com/www.amazon.com/Kindle-Wireless-Reader-Wifi-Graphite/dp/B002Y27P3M/507846.html",
  "http://localhost:8009/tp5/linkedin.com/www.linkedin.com/in/christopherblizzard@goback=.nppvan_%252Flemuelf.html",
  "http://localhost:8010/tp5/bing.com/www.bing.com/search@q=mozilla&go=&form=QBLH&qs=n&sk=&sc=8-0.html",
  "http://localhost:8011/tp5/icanhascheezburger.com/icanhascheezburger.com/index.html",
  "http://localhost:8012/tp5/yandex.ru/yandex.ru/yandsearch@text=mozilla&lr=21215.html",
  "http://localhost:8013/tp5/cgi.ebay.com/cgi.ebay.com/ALL-NEW-KINDLE-3-eBOOK-WIRELESS-READING-DEVICE-W-WIFI-/130496077314@pt=LH_DefaultDomain_0&hash=item1e622c1e02.html",
  "http://localhost:8014/tp5/163.com/www.163.com/index.html",
  "http://localhost:8015/tp5/mail.ru/mail.ru/index.html",
  "http://localhost:8016/tp5/bbc.co.uk/www.bbc.co.uk/news/index.html",
  "http://localhost:8017/tp5/store.apple.com/store.apple.com/us@mco=Nzc1MjMwNA.html",
  "http://localhost:8018/tp5/imdb.com/www.imdb.com/title/tt1099212/index.html",
  "http://localhost:8019/tp5/mozilla.com/www.mozilla.com/en-US/firefox/all-older.html",
  "http://localhost:8020/tp5/ask.com/www.ask.com/web@q=What%27s+the+difference+between+brown+and+white+eggs%253F&gc=1&qsrc=3045&o=0&l=dir.html",
  "http://localhost:8021/tp5/cnn.com/www.cnn.com/index.html",
  "http://localhost:8022/tp5/sohu.com/www.sohu.com/index.html",
  "http://localhost:8023/tp5/vkontakte.ru/vkontakte.ru/help.php@page=about.html",
  "http://localhost:8024/tp5/youku.com/www.youku.com/index.html",
  "http://localhost:8025/tp5/myparentswereawesome.tumblr.com/myparentswereawesome.tumblr.com/index.html",
  "http://localhost:8026/tp5/ifeng.com/ifeng.com/index.html",
  "http://localhost:8027/tp5/ameblo.jp/ameblo.jp/index.html",
  "http://localhost:8028/tp5/tudou.com/www.tudou.com/index.html",
  "http://localhost:8029/tp5/chemistry.about.com/chemistry.about.com/index.html",
  "http://localhost:8030/tp5/beatonna.livejournal.com/beatonna.livejournal.com/index.html",
  "http://localhost:8031/tp5/hao123.com/hao123.com/index.html",
  "http://localhost:8032/tp5/rakuten.co.jp/www.rakuten.co.jp/index.html",
  "http://localhost:8033/tp5/alibaba.com/www.alibaba.com/product-tp/101509462/World_s_Cheapest_Laptop.html",
  "http://localhost:8034/tp5/uol.com.br/www.uol.com.br/index.html",
  "http://localhost:8035/tp5/cnet.com/www.cnet.com/index.html",
  "http://localhost:8036/tp5/ehow.com/www.ehow.com/how_4575878_prevent-fire-home.html",
  "http://localhost:8037/tp5/thepiratebay.org/thepiratebay.org/top/201.html",
  "http://localhost:8038/tp5/page.renren.com/page.renren.com/index.html",
  "http://localhost:8039/tp5/chinaz.com/chinaz.com/index.html",
  "http://localhost:8040/tp5/globo.com/www.globo.com/index.html",
  "http://localhost:8041/tp5/spiegel.de/www.spiegel.de/index.html",
  "http://localhost:8042/tp5/dailymotion.com/www.dailymotion.com/us.html",
  "http://localhost:8043/tp5/goo.ne.jp/goo.ne.jp/index.html",
  "http://localhost:8044/tp5/alipay.com/www.alipay.com/index.html",
  "http://localhost:8045/tp5/stackoverflow.com/stackoverflow.com/questions/184618/what-is-the-best-comment-in-source-code-you-have-ever-encountered.html",
  "http://localhost:8046/tp5/nicovideo.jp/www.nicovideo.jp/index.html",
  "http://localhost:8047/tp5/ezinearticles.com/ezinearticles.com/index.html@Migraine-Ocular---The-Eye-Migraines&id=4684133.html",
  "http://localhost:8048/tp5/taringa.net/www.taringa.net/index.html",
  "http://localhost:8049/tp5/tmall.com/www.tmall.com/index.html@ver=2010s.html",
  "http://localhost:8050/tp5/huffingtonpost.com/www.huffingtonpost.com/index.html",
  "http://localhost:8051/tp5/deviantart.com/www.deviantart.com/index.html",
  "http://localhost:8052/tp5/media.photobucket.com/media.photobucket.com/image/funny%20gif/findstuff22/Best%20Images/Funny/funny-gif1.jpg@o=1.html",
  "http://localhost:8053/tp5/douban.com/www.douban.com/index.html",
  "http://localhost:8054/tp5/imgur.com/imgur.com/gallery/index.html",
  "http://localhost:8055/tp5/reddit.com/www.reddit.com/index.html",
  "http://localhost:8056/tp5/digg.com/digg.com/news/story/New_logo_for_Mozilla_Firefox_browser.html",
  "http://localhost:8057/tp5/filestube.com/www.filestube.com/t/the+vampire+diaries.html",
  "http://localhost:8058/tp5/dailymail.co.uk/www.dailymail.co.uk/ushome/index.html",
  "http://localhost:8059/tp5/whois.domaintools.com/whois.domaintools.com/mozilla.com.html",
  "http://localhost:8060/tp5/indiatimes.com/www.indiatimes.com/index.html",
  "http://localhost:8061/tp5/rambler.ru/www.rambler.ru/index.html",
  "http://localhost:8062/tp5/torrentz.eu/torrentz.eu/search@q=movies.html",
  "http://localhost:8063/tp5/reuters.com/www.reuters.com/index.html",
  "http://localhost:8064/tp5/foxnews.com/www.foxnews.com/index.html",
  "http://localhost:8065/tp5/xinhuanet.com/xinhuanet.com/index.html",
  "http://localhost:8066/tp5/56.com/www.56.com/index.html",
  "http://localhost:8067/tp5/bild.de/www.bild.de/index.html",
  "http://localhost:8068/tp5/guardian.co.uk/www.guardian.co.uk/index.html",
  "http://localhost:8069/tp5/w3schools.com/www.w3schools.com/html/default.asp.html",
  "http://localhost:8070/tp5/naver.com/www.naver.com/index.html",
  "http://localhost:8071/tp5/blogfa.com/blogfa.com/index.html",
  "http://localhost:8072/tp5/terra.com.br/www.terra.com.br/portal/index.html",
  "http://localhost:8073/tp5/ucoz.ru/www.ucoz.ru/index.html",
  "http://localhost:8074/tp5/yelp.com/www.yelp.com/biz/alexanders-steakhouse-cupertino.html",
  "http://localhost:8075/tp5/wsj.com/online.wsj.com/home-page.html",
  "http://localhost:8076/tp5/noimpactman.typepad.com/noimpactman.typepad.com/index.html",
  "http://localhost:8077/tp5/myspace.com/www.myspace.com/albumart.html",
  "http://localhost:8078/tp5/google.com/www.google.com/search@q=mozilla.html",
  "http://localhost:8079/tp5/orange.fr/www.orange.fr/index.html",
  "http://localhost:8080/tp5/php.net/php.net/index.html",
  "http://localhost:8081/tp5/zol.com.cn/www.zol.com.cn/index.html",
  "http://localhost:8082/tp5/mashable.com/mashable.com/index.html",
  "http://localhost:8083/tp5/etsy.com/www.etsy.com/category/geekery/videogame.html",
  "http://localhost:8084/tp5/gmx.net/www.gmx.net/index.html",
  "http://localhost:8085/tp5/csdn.net/csdn.net/index.html",
  "http://localhost:8086/tp5/xunlei.com/xunlei.com/index.html",
  "http://localhost:8087/tp5/hatena.ne.jp/www.hatena.ne.jp/index.html",
  "http://localhost:8088/tp5/icious.com/www.delicious.com/index.html",
  "http://localhost:8089/tp5/repubblica.it/www.repubblica.it/index.html",
  "http://localhost:8090/tp5/web.de/web.de/index.html",
  "http://localhost:8091/tp5/slideshare.net/www.slideshare.net/jameswillamor/lolcats-in-popular-culture-a-historical-perspective.html",
  "http://localhost:8092/tp5/telegraph.co.uk/www.telegraph.co.uk/index.html",
  "http://localhost:8093/tp5/seesaa.net/blog.seesaa.jp/index.html",
  "http://localhost:8094/tp5/wp.pl/www.wp.pl/index.html",
  "http://localhost:8095/tp5/aljazeera.net/aljazeera.net/portal.html",
  "http://localhost:8096/tp5/w3.org/www.w3.org/standards/webdesign/htmlcss.html",
  "http://localhost:8097/tp5/homeway.com.cn/www.hexun.com/index.html",
  "http://localhost:8098/tp5/facebook.com/www.facebook.com/Google.html",
  "http://localhost:8099/tp5/youtube.com/www.youtube.com/music.html",
  "http://localhost:8100/tp5/people.com.cn/people.com.cn/index.html"
];


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
        }
    },
    'linux': {
        'Chrome': {
            'binary': '/usr/bin/google-chrome-unstable',
            'parent_filter': lambda x: 'chrome --type' not in x,
            'path_filter': lambda x: 'chrome-unstable' in x
        },
        'Firefox': {
            'binary': '/home/erahm/dev/comp_analysis/firefox/firefox-bin',
            'parent_filter': lambda x: 'firefox-bin' in x,
            'path_filter': lambda x: 'comp_analysis/firefox' in x
        }
    },
}

def test_browser(browser, quick=False):
  config = SETUP[mozinfo.os][browser]
  stats = ProcessStats(config['path_filter'], config['parent_filter'])

  if quick:
    urls = TEST_SITES[:3]
    test_options = {
      'per_tab_pause': 1,
      'settle_wait_time': 0
    }
  else:
    urls = TEST_SITES[:30]
    test_options = {
      'per_tab_pause': 10,
      'settle_wait_time': 60
    }

  if browser == 'Chrome':
    options = webdriver.chrome.options.Options()
    options.binary_location = config['binary']
    driver = webdriver.Chrome(chrome_options=options)

    test = MultiTabTest(driver, stats, **test_options)
    test.open_urls(urls)

    driver.quit()
  elif browser == 'Firefox':
    test = FirefoxMultiTabTest(config['binary'], stats, **test_options)
    test.open_urls(urls)
  elif browser == 'IE':
    # Roughly what we would do if we could do:
    #driver = webdriver.Ie()
    #test = MultiTabTest(driver, stats)
    #test.open_urls(TEST_SITES[:30], tab_limit=30, settle_wait_time=60)
    #driver.quit()
    raise Exception("IE is not implemented yet.")
  else:
    raise Exception("Unhandled browser: %s" % browser)

# Left for posterity, someday this might work:
#elif browser == "FirefoxActuallyWorks":
  # This is busted for several reasons:
  #   - wires doesn't support setting preferences
  #     https://github.com/jgraham/wires/issues/27
  #   - wires doesn't support e10s
  #     https://github.com/jgraham/wires/issues/43
#  firefox_profile = webdriver.FirefoxProfile()
#  # Make sure e10s is *really* enabled.
#  firefox_profile.set_preference("browser.tabs.remote.autostart", True)
#  firefox_profile.set_preference("browser.tabs.remote.autostart1", True)
#  firefox_profile.set_preference("browser.tabs.remote.autostart2", True)
#  firefox_profile.set_preference("browser.tabs.remote.autostart3", True)
#  firefox_profile.set_preference("browser.tabs.remote.autostart4", True)
#  firefox_profile.set_preference("browser.tabs.remote.autostart5", True)
#  firefox_profile.set_preference("browser.tabs.remote.autostart6", True)
#  firefox_profile.set_preference("browser.tabs.remote.autostart7", True)
#  # Specify the number of content processes.
#  firefox_profile.set_preference("dom.ipc.processCount", 1)
#  # Don't tell us we're using e10s.
#  firefox_profile.set_preference("browser.displayedE10SNotice", 1000)
#
#  firefox_capabilities = DesiredCapabilities.FIREFOX.copy()
#  firefox_capabilities['marionette'] = True
  #firefox_capabilities['firefox_profile'] = firefox_profile.encoded
  #firefox_capabilities['binary'] = '/Applications/FirefoxNightly.app/Contents/MacOS/firefox'
#  firefox_capabilities.update(SETUP[mozinfo.os]['Firefox'])
#
#  driver = webdriver.Firefox(capabilities=firefox_capabilities)

test_browser("Chrome")
test_browser("Firefox")

if mozinfo.os == "win":
  #test_browser("IE")
  pass
elif mozinfo.os == "mac":
  #test_browser("Safari")
  pass
