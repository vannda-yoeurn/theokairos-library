#!/bin/sh
# Copy the library website into the app (run from app/)
set -e
rm -rf www && mkdir www
cp ../index.html www/
cp -r ../books ../covers www/
