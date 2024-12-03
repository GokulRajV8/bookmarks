import os
import threading

from . import DBEngine


class Service:
    def __init__(self, db_file: str, db_lock: threading.Lock):
        if os.path.isfile(db_file):
            self.__db_engine = DBEngine(db_file, db_lock)
        else:
            open(db_file, "w").close()
            self.__db_engine = DBEngine(db_file, db_lock)
            self.__db_engine.create_tables()

    def create_site(self, site_name: str, site_url: str, tags: list[str]):
        site_id = self.__db_engine.insert_site(site_name, site_url)
        for tag in tags:
            tag_id = self.__db_engine.get_tag_id(tag)
            self.__db_engine.map_site_tag(site_id, tag_id)

    def read_site(self, site_id: str) -> tuple:
        return self.__db_engine.get_site(site_id)

    def read_sites(self, tags: list[str]) -> list[tuple]:
        sites = self.__db_engine.get_sites(tags)
        return sites

    def update_site(self, site_id: str, site_name: str, site_url: str, tags: list[str]):
        is_present = self.__db_engine.update_site(site_id, site_name, site_url)
        if not is_present:
            return

        self.__db_engine.delete_tags_map(site_id)
        for tag in tags:
            tag_id = self.__db_engine.get_tag_id(tag)
            self.__db_engine.map_site_tag(site_id, tag_id)

    def delete_site(self, site_id: str):
        self.__db_engine.delete_tags_map(site_id)
        self.__db_engine.delete_site(site_id)

    def close(self):
        self.__db_engine.close()
