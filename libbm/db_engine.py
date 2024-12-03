import sqlite3
import sys


class DBEngine:
    def __init__(self, db_file: str):
        self.__db_connection = sqlite3.connect(db_file)
        self.__db_cursor = self.__db_connection.cursor()

    def create_tables(self):
        self.__db_cursor.execute(
            "CREATE TABLE sites (id integer PRIMARY KEY autoincrement, name text, url text)"
        )
        self.__db_cursor.execute(
            "CREATE TABLE tags (id integer PRIMARY KEY autoincrement, name text, UNIQUE(name))"
        )
        self.__db_cursor.execute(
            "CREATE TABLE site_tag_map (site_id integer, tag_id integer, FOREIGN KEY(site_id) REFERENCES sites(id), FOREIGN KEY(tag_id) REFERENCES tags(id))"
        )

    def __read_one(self, query: str, params: tuple) -> tuple:
        try:
            result = self.__db_cursor.execute(query, params).fetchone()
            return result
        except sqlite3.Error as e:
            print(e.args)
            sys.exit(1)

    def __read_many(self, query: str, params: tuple) -> list[tuple]:
        try:
            result = self.__db_cursor.execute(query, params).fetchall()
            return result
        except sqlite3.Error as e:
            print(e.args)
            sys.exit(1)

    def __read_many_single_column(self, query: str, params: tuple) -> list:
        result = self.__read_many(query, params)
        return [val[0] for val in result]

    def __write(self, query: str, params: tuple):
        try:
            self.__db_cursor.execute(query, params)
            self.__db_connection.commit()
        except sqlite3.Error as e:
            print(e.args)
            sys.exit(1)

    def get_tag_id(self, tag_name: str) -> int:
        result = self.__read_one("SELECT id FROM tags WHERE name = ?", (tag_name,))

        if result is None:
            self.__write("INSERT INTO tags(name) VALUES(?)", (tag_name,))
            result = self.__read_one(
                "SELECT seq FROM sqlite_sequence WHERE name = ?", ("tags",)
            )

        return result[0]

    def insert_site(self, site_name: str, site_url: str) -> int:
        self.__write("INSERT INTO sites(name, url) VALUES(?, ?)", (site_name, site_url))
        result = self.__read_one(
            "SELECT seq FROM sqlite_sequence WHERE name = ?", ("sites",)
        )

        return result[0]

    def map_site_tag(self, site_id: int, tag_id: int):
        self.__write(
            "INSERT INTO site_tag_map(site_id, tag_id) VALUES(?, ?)", (site_id, tag_id)
        )

    def get_site(self, site_id: str) -> tuple:
        self.__read_one("SELECT id, name, url FROM sites WHERE id = ?", (site_id,))

    def get_sites(self, tags: list[str]) -> list[tuple]:
        tags_count = len(tags)
        if tags_count == 0:
            return []

        sites = self.__read_many_single_column("SELECT id FROM sites", ())
        for tag in tags:
            new_sites = self.__read_many_single_column(
                "SELECT s.id FROM sites s, tags t, site_tag_map stm WHERE stm.site_id = s.id AND stm.tag_id = t.id AND t.name = ?",
                (tag,),
            )
            sites = [site for site in sites if site in new_sites]

        query_component = "?, " * len(sites)
        result = self.__read_many(
            f"SELECT id, name, url FROM sites WHERE id in ({query_component[:-2]})",
            tuple(sites),
        )

        return result

    def update_site(self, site_id: str, site_name: str, site_url: str) -> bool:
        rcount = self.__read_many("SELECT id FROM sites WHERE id = ?", (site_id,))
        if len(rcount) == 0:
            return False

        self.__write(
            "UPDATE sites SET name = ?, url = ? WHERE id = ?",
            (site_name, site_url, site_id),
        )
        return True

    def delete_tags_map(self, site_id: str):
        self.__write("DELETE FROM site_tag_map WHERE site_id = ?", (site_id,))

    def delete_site(self, site_id: str):
        self.__write("DELETE FROM sites WHERE id = ?", (site_id,))

    def close(self):
        self.__db_cursor.close()
        self.__db_connection.close()
