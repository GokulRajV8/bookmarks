#!/bin/bash

case $1 in
    start)
        if pgrep gunicorn > /dev/null 2>&1; then
            echo 'Already gunicorn server running'
        else
            source .venv/bin/activate
            gunicorn server:app & > /dev/null 2>&1
            echo 'Started gunicorn server'
        fi
        ;;
    stop)
        if [ ! -f parent.pid ]; then
            echo 'No gunicorn server running'
        else
            kill -SIGTERM `cat parent.pid`
            echo 'Stopped gunicorn server'
            rm parent.pid access.log
        fi
        ;;
    *)
        echo 'Invalid option. Enter start/stop'
        ;;
esac
