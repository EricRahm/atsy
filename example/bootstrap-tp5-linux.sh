#!/usr/bin/env bash

# Install a local webserver
if ! dpkg -l nginx | grep -q nginx ; then
    echo "Installing nginx"
    sudo apt-get install nginx
fi

# Install virtualenv if necessary
if ! [ which virtualenv > /dev/null ]; then
    pip install virtualenv
fi

mkdir atsy-test
cd atsy-test

# Setup a virtualenv to work in
virtualenv venv
source venv/bin/activate

# Setup atsy
git clone https://github.com/EricRahm/atsy.git
cd atsy
python setup.py install
cd ..

# Get the latest chromedriver
CHROMEDRIVER_VERSION=$(curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip

# Download the tp5 pageset and setup a webroot
mkdir nginx_root
cd nginx_root

mkdir html
mkdir logs
mkdir conf

# Install tp5
wget http://people.mozilla.org/~jmaher/taloszips/zips/tp5n.zip
unzip tp5n.zip -d html/
rm tp5n.zip

# Add the nginx config
cp ../atsy/example/comp_analysis_nginx.conf conf/nginx.conf

deactivate

echo "Setup finished!"
