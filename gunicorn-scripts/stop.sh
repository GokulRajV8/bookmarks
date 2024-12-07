#!/usr/bin/bash

cd ~/apps/bookmarks-server

if [ -f parent.pid ]; then
        kill -9 `cat parent.pid`
        echo 'Stopped gunicorn server'
        rm parent.pid access.log
else
        echo 'No gunicorn server to stop'
fi
