/*drop table if exists Profiles; */
create table Accounts (
    id          Serial,
    name		text 		not null,
	email       text 		not null 	unique,
	password 	text 		not null,
	primary key (id)
);
/* Need to add constraint to email design */


/* This is temporary, it should not reference account but rather profile*/
create table Recipes (
    id          Serial      not null,
    name        text        not null,
    description text        not null,

    owner       Serial      not null references Accounts(id),
    primary key (id)
);
