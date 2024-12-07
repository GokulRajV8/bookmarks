#!/usr/bin/bash

cd ~/apps/bookmarks-server

source .venv/bin/activate

if pgrep gunicorn > /dev/null 2>&1; then
        echo 'Already gunicorn server running'
else
        gunicorn server:app & > /dev/null 2>&1
        echo 'Started gunicorn server'
fi
