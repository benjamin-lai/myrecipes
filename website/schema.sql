create table Users (
    id          Serial      Primary key,
    first_name  text        not null,
    email       text 		not null 	unique,
	password 	text 		not null
);

CREATE TABLE Images(  
    id          Serial      Primary key,  
    image_name  text        not null,
    image_data  bytea       not null,
    username    text        not null       
);
