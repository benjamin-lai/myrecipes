create table Users (
    id          Serial      Primary key,
    first_name  text        not null,
    email       text 		not null 	unique,
	password 	text 		not null
);

create table Recipes (
    id              serial      primary key,
    name            text        not null,
    description     text        not null,
    photo           text,
    serving         int         not null,
    creates         integer     not null,   -- users.id
    foreign key (creates) references Users(id)     
);

create table Ingredient (
    recipe_id integer references Recipes(id),
    ingredient      text,
    dosage          int,
    unit_name       text,       
    primary key(recipe_id, ingredient)
);

create table RecipeStep(
    recipe_id       integer references Recipes(id),
    step_no         int     not null,
    step_comment    text    not null,
    photo           text,
    primary key(recipe_id, step_no)
);