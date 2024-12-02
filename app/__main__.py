from .db_engine import DBEngine


def insert_data(db_engine: DBEngine):
    site_name = input("Enter site title : ")
    site_url = input("Enter site URL : ")

    tags = input("Enter tags (space-separated): ")
    tags = tags.split()

    site_id = db_engine.insert_site(site_name, site_url)
    for tag in tags:
        tag_id = db_engine.insert_tag(tag)
        db_engine.map_site_tag(site_id, tag_id)


def read_data(db_engine: DBEngine):
    tags = input("Enter tags (space-separated): ")
    tags = tags.split()

    sites = db_engine.get_sites(tags)
    print()
    for site in sites:
        print(f"Name : {site[0]}")
        print(f"URL : {site[1]}")
        print()


if __name__ == "__main__":
    db_engine = DBEngine("C:\\Users\\gokul\\Databases\\bookmarks.db")

    print()
    print("    1. Enter data")
    print("    2. Read data")
    print()
    option = input("Enter option : ")
    print()

    match option:
        case "1":
            insert_data(db_engine)
        case "2":
            read_data(db_engine)

    db_engine.close()
