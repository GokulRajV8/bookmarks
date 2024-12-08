# Bookmarks

Save URL bookmarks using tag based system

## Requirements

1. Any Linux based distro
2. Python>=3.8
3. Gunicorn server
4. Nginx server

## Installation

This is a web-based application and I have used Gunicorn as application (API) server and Nginx as web server for application proxy and to server static content.

1. Create a directory called `bookmarks-app` and run the below commands inside it.

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install git+https://github.com/GokulRajV8/bookmarks gunicorn
    ```

2. Copy the contents in gunicorn-scripts to the app directory. The app directory should look like below. You can start and stop the server using [server.sh](gunicorn-scripts/server.sh) script.

    ```
    bookmarks-app/
        .venv/
        gunicorn.conf.py
        server.sh
    ```

3. Copy the contents in web directory somewhere so that it can be served as static content using Nginx alias. I have used `/bookmarks` alias to web directory. This alias should match with the value of `Constants.APP` in [main.js](web/static/js/main.js).

4. Now that static content is served and API server is running, last step is to add Nginx proxy to our gunicorn server. Here our gunicorn server is running on port 4000, so we have added a proxy entry in Nginx server to forward requests to this port. We are using `/bookmarks/api` as our API server endpoint (can be seen as value of `Constants.API` in [__init__.py](server/__init__.py) and [main.js](web/static/js/main.js)) and hence the same is added as proxy entry in Nginx server.

5. Make sure that the constants in [__init__.py](server/__init__.py) and [main.js](web/static/js/main.js) are the same so that API call from static webpages will be routed correctly to our gunicorn server.