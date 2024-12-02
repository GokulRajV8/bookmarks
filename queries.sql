CREATE TABLE sites (
	id integer PRIMARY KEY autoincrement,
	name text,
	url text
);

CREATE TABLE tags (
	id integer PRIMARY KEY autoincrement,
	name text,
	unique(name)
);

CREATE TABLE site_tag_map (
	site_id integer,
	tag_id integer,
	FOREIGN KEY(site_id) REFERENCES sites(id),
	FOREIGN KEY(tag_id) REFERENCES tags(id)
);

SELECT * FROM sites;

SELECT * FROM tags;

SELECT * FROM site_tag_map;

select * from sqlite_sequence;
