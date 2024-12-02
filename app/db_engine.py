import sqlite3


class DBEngine:
    def __init__(self, db_file: str):
        self.__db_connection = sqlite3.connect(db_file)
        self.__db_cursor = self.__db_connection.cursor()

    def insert_tag(self, tag_name: str) -> int:
        try:
            query = "SELECT id FROM tags WHERE name = ?"
            result = self.__db_cursor.execute(query, (tag_name,)).fetchone()

            if result is None:
                query = "INSERT INTO tags(name) VALUES(?)"
                self.__db_cursor.execute(query, (tag_name,))
                self.__db_connection.commit()

                query = "SELECT seq FROM sqlite_sequence WHERE name = ?"
                result = self.__db_cursor.execute(query, ("tags",)).fetchone()

            return result[0]

        except sqlite3.Error as e:
            print(e.args)

    def insert_site(self, site_name: str, site_url: str) -> int:
        try:
            query = "INSERT INTO sites(name, url) VALUES(?, ?)"
            self.__db_cursor.execute(query, (site_name, site_url))
            self.__db_connection.commit()

            query = "SELECT seq FROM sqlite_sequence WHERE name = ?"
            result = self.__db_cursor.execute(query, ("sites",)).fetchone()
            return result[0]

        except sqlite3.Error as e:
            print(e.args)

    def map_site_tag(self, site_id: int, tag_id: int):
        try:
            query = "INSERT INTO site_tag_map(site_id, tag_id) VALUES(?, ?)"
            self.__db_cursor.execute(query, (site_id, tag_id))
            self.__db_connection.commit()

        except sqlite3.Error as e:
            print(e.args)

    def get_sites(self, tags: list[str]) -> list[tuple]:
        try:
            tags_count = len(tags)
            query_component = "?, " * tags_count
            query = f"SELECT s.name, s.url FROM sites s, tags t, site_tag_map stm WHERE stm.site_id = s.id AND stm.tag_id = t.id AND t.name IN ({query_component[:-2]})"
            result = self.__db_cursor.execute(query, tuple(tags)).fetchall()
            return result

        except sqlite3.Error as e:
            print(e.args)

    def close(self):
        self.__db_cursor.close()
        self.__db_connection.close()
