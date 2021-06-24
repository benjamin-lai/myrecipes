create table Users (
    id          Serial      Primary key,
    first_name  text        not null,
    email       text 		not null 	unique,
	password 	text 		not null
);