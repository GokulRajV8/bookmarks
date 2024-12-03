"""
Server package for web version
"""

import os
import threading

from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Api
from flask_restful import Resource

from libbm import Service as BMService

# creating objects
db_lock = threading.Lock()
bm_service = BMService(
    os.path.join(os.environ["USERPROFILE"], "Databases", "bookmarks.db"), db_lock
)


class SiteResource(Resource):
    def generate_site_data(self, id: str, title: str, url: str) -> dict:
        result = {}
        result["id"] = id
        result["title"] = title
        result["url"] = url

        return result

    def get_sites_from_tags(self, tags: list[str]) -> list:
        result = bm_service.read_sites(tags)
        response = []
        for site in result:
            response.append(self.generate_site_data(site[0], site[1], site[2]))

        return response

    def get_site_from_id(self, site_id: str) -> dict:
        site = bm_service.read_site(site_id)
        if site is not None:
            return self.generate_site_data(site[0], site[1], site[2])
        else:
            return {}

    def post(self):
        if (
            len(request.form) != 3
            or "name" not in request.form
            or "url" not in request.form
            or "tags" not in request.form
        ):
            return None, 400

        site_name = request.form["name"]
        site_url = request.form["url"]
        tags = request.form["tags"].split()

        bm_service.create_site(site_name, site_url, tags)
        return None, 200

    def get(self):
        response = None
        if len(request.args) == 1:
            key = list(request.args.keys())[0]
            val = request.args[key]
            match key:
                case "id":
                    response = self.get_site_from_id(val)
                case "tags":
                    response = self.get_sites_from_tags(val.split())
            response = jsonify(response) if response is not None else None

        if response is None:
            return None, 400
        else:
            return response

    def put(self):
        if (
            len(request.form) != 3
            or "name" not in request.form
            or "url" not in request.form
            or "tags" not in request.form
        ):
            return None, 400

        if len(request.args) != 1 or "id" not in request.args:
            return None, 400

        site_id = request.args["id"]
        site_name = request.form["name"]
        site_url = request.form["url"]
        tags = request.form["tags"].split()

        bm_service.update_site(site_id, site_name, site_url, tags)
        return None, 200

    def delete(self):
        response = None
        if len(request.args) == 1:
            key = list(request.args.keys())[0]
            val = request.args[key]
            match key:
                case "id":
                    bm_service.delete_site(val)
                    response = None, 200

        if response is None:
            return None, 400
        else:
            return response


class TagResource(Resource):
    def get(self):
        response = bm_service.read_tags()
        return jsonify(response)


# creating app and api and mapping resources
app = Flask("bookmarks-manager-api")
api = Api(app)
api.add_resource(SiteResource, "/api/site", endpoint="api/site")
api.add_resource(TagResource, "/api/tags", endpoint="api/tags")
