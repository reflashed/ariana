#!/bin/bash

CURR_DIR=`cd $(dirname $BASH_SOURCE) && pwd`
export GOOGLE_APPLICATION_CREDENTIALS="$CURR_DIR/gcloud-key.json"
python3 go.py
