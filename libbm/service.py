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

    def __update_tags(self, site_id: str, tags: list[str]):
        case_insensitive_tags = [tag.lower() for tag in tags]
        for tag in case_insensitive_tags:
            tag_id = self.__db_engine.get_tag_id(tag)
            self.__db_engine.map_site_tag(site_id, tag_id)

    def create_site(self, site_name: str, site_url: str, tags: list[str]):
        site_id = self.__db_engine.insert_site(site_name, site_url)
        self.__update_tags(site_id, tags)

    def read_site(self, site_id: str) -> tuple:
        site_data = self.__db_engine.get_site(site_id)
        site_tags = self.__db_engine.get_tags_for_site(site_id)

        return *site_data, " ".join(site_tags)

    def read_sites(self, tags: list[str]) -> list[tuple]:
        case_insensitive_tags = [tag.lower() for tag in tags]
        sites = self.__db_engine.get_sites(case_insensitive_tags)
        return sites

    def update_site(self, site_id: str, site_name: str, site_url: str, tags: list[str]):
        is_present = self.__db_engine.update_site(site_id, site_name, site_url)
        if not is_present:
            return

        self.__db_engine.delete_tags_map(site_id)
        self.__update_tags(site_id, tags)

    def delete_site(self, site_id: str):
        self.__db_engine.delete_tags_map(site_id)
        self.__db_engine.delete_site(site_id)

    def read_tags(self):
        tags = self.__db_engine.get_tags().sort()
        return tags

    def close(self):
        self.__db_engine.close()
