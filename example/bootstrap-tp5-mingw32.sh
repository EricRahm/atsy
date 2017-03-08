#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$0")

# Assumes you have pip, wget

mkdir atsy-test
cd atsy-test

# Clone the atsy repo
# Manually git clone atsy
#git clone https://github.com/EricRahm/atsy.git

# Install nginx for windows
NGINX_ZIP=nginx-1.11.10.zip
wget http://nginx.org/download/$NGINX_ZIP
unzip $NGINX_ZIP
rm $NGINX_ZIP

# Get the latest chromedriver
CHROMEDRIVER_ZIP=chromedriver_win32.zip
CHROMEDRIVER_VERSION=$(wget -qO- http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/$CHROMEDRIVER_ZIP
unzip $CHROMEDRIVER_ZIP
rm $CHROMEDRIVER_ZIP

# Download the tp5 pageset and setup a webroot
mkdir nginx_root
cd nginx_root

mkdir html
mkdir logs
mkdir conf

# Install tp5
wget http://people.mozilla.org/~jmaher/taloszips/zips/tp5n.zip
unzip -q tp5n.zip -d html/
mv html/tp5n/ html/tp5
rm tp5n.zip

# Add the nginx config
cp "../../$SCRIPT_DIR/comp_analysis_nginx.conf" conf/nginx.conf

cd ..

#########################
# Setup python pacakges #
#########################

# Install virtualenv if necessary
pip install virtualenv

# Setup a virtualenv to work in
virtualenv venv
source venv/Scripts/activate

# For installing Firefox nightly
pip install mozdownload mozinstall

# Setup atsy
cd "../$SCRIPT_DIR/.." 
python setup.py install
cd -

deactivate

echo "Setup finished!"
