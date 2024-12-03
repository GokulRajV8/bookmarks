import os

from libbm import Service

MSG_ENTER_OPTION = "Enter option : "
MSG_ENTER_ID = "Enter site id : "
MSG_ENTER_TITLE = "Enter site title : "
MSG_ENTER_URL = "Enter site URL : "
MSG_ENTER_TAGS = "Enter tags (space-separated): "


def create_site(service: Service):
    print()
    site_name = input(MSG_ENTER_TITLE)
    site_url = input(MSG_ENTER_URL)
    tags = input(MSG_ENTER_TAGS)
    tags = tags.split()

    service.create_site(site_name, site_url, tags)


def read_sites(service: Service):
    print()
    tags = input(MSG_ENTER_TAGS)
    tags = tags.split()

    sites = service.read_sites(tags)
    for site in sites:
        print()
        print(f"ID : {site[0]}\nTitle : {site[1]}\nURL : {site[2]}")


def update_site(service: Service):
    print()
    site_id = input(MSG_ENTER_ID)
    site_name = input(MSG_ENTER_TITLE)
    site_url = input(MSG_ENTER_URL)
    tags = input(MSG_ENTER_TAGS)
    tags = tags.split()

    service.update_site(site_id, site_name, site_url, tags)


def delete_site(service: Service):
    print()
    site_id = input(MSG_ENTER_ID)
    service.delete_site(site_id)


if __name__ == "__main__":
    # database file will be ~/Databases/bookmarks.db
    db_file = os.path.join(os.environ["USERPROFILE"], "Databases", "bookmarks.db")
    service = Service(db_file)

    print()
    print("    1. Create site")
    print("    2. Read sites")
    print("    3. Update site")
    print("    4. Delete site")
    print("    Any other to exit")

    while True:
        print()
        option = input(MSG_ENTER_OPTION)

        match option:
            case "1":
                create_site(service)
            case "2":
                read_sites(service)
            case "3":
                update_site(service)
            case "4":
                delete_site(service)
            case _:
                break

    service.close()
