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

create table recipe(
    id          serial      primary key,
    name        text        not null,
    description text        not null,
    image       bytea       not null,
    creates     integer     not null,
    foreign     key (creates) references Users(id) 
);

create table Ingredient (
    recipe_id integer references Recipes(id),
    ingredient        text,
    primary key(recipe_id, ingredient)
);

create table RecipeStep(
    recipe_id        integer references Recipes(id),
    step_no          int     not null,
    step_comment     text    not null, 
    primary key(recipe_id, step_no)
);

