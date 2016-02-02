# atsy
A dumping ground for cross-platform browser memory testing.

## Example Usage
An example script can be found under `example/comp_analysis.py`. It uses the TP5 pageset which currently is not public, but the example can be modified to use any set of URLs.

### Prereqs
- nginx
- The latest [chromedriver](http://chromedriver.storage.googleapis.com/index.html) and unarchive it.
- Install **atsy**: `python setup.py install` should do the trick.
- Install/update the browsers you want to test. Note installation locations.
- Update the setup portion of the example to specify your binary locations and update the path filters if necessary.
- Setup a proxy server to silently kill all outbound requests.

### Running
1. Launch your proxy server (this is only really necessary for Firefox)
2. Launch nginx, I use the config from awsy, so something like `nginx -p nginx/ -c conf/nginx.conf`
3. Launch the example, this assumes chromedriver is in the cwd: `$PATH=$PATH:. python example/comp_analysis.py`
