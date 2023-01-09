#!/bin/bash
sudo pip install -U \
     boto3 \
     singledispatch
sudo python -m nltk.downloader -d /usr/share/nltk_data all
