create table Users (
    id              serial      primary key,
	password 	    text 		check (length(password) > 5) not null,  -- or check through python code?
    email           text 		check (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$') not null unique
);

create table Profiles (
    profile_id      serial      primary key,
    first_name      text        not null,
    last_name       text        not null,
    display_name    text        not null,
    profile_pic     text        not null,   --default blank or something
    temp_pic        text,
    bio             text,
    owns            integer     not null,   -- user.id  = profile.id =  owns? may be redundant, just mapping how its shown through 3311
    foreign key (owns) references Users(id) -- or just change owns to profile_id or something as use that as the relation.
);

create table Recipes (
    id              serial      primary key,
    name            text        not null,
    description     text        not null,
    photo           text        not null,
    creates         integer     not null,
    foreign key (creates) references Users(id)     -- users.id
);

create table Ingredient (
    recipe_id integer references Recipes(id),
    ingredient     text,
    primary key(recipe_id, ingredient)
);

create table Method (
    recipe_id integer references Recipes(id),
    method     text,
    primary key(recipe_id, method)
);

create table Meal_Type (
    recipe_id integer references Recipes(id),
    meal_type     text,
    primary key(recipe_id, meal_type)
);


-- list of people that are subscribed to the profile (contains)
create table Subscriber_Lists (
    subscriber_id   integer     not null,
    contains        integer     not null,   -- contains is profile_id
    primary key (subscriber_id, contains),
    foreign key (contains) references Profiles(profile_id)
);

-- list of people that the profile (contains) is subscribed to
create table Subscribed_To_Lists (
    subscribed_id   integer      not null,
    contains        integer     not null,   -- contains is profile_id
    primary key (subscribed_id, contains),
    foreign key (contains) references Profiles(profile_id)
);

create table CookBooks_Lists (
    cookbook_id     integer      not null,
    recipe_id       integer      not null,
    contains        integer     not null,   -- contains is profile_id
    primary key (cookbook_id, recipe_id, contains),   -- duplicate recipes cant be put into the same cookbook for a given user
    foreign key (contains) references Profiles(profile_id),
    foreign key (recipe_id) references Recipes(id)      -- added this line, but not sure if necessary, will just check if the id exists in recipes
);

create table History_Lists (
    recipe_id       integer      not null,
    contains        integer     not null,   -- contains is profile_id
    primary key (recipe_id, contains),
    foreign key (contains) references Profiles(profile_id),
    foreign key (recipe_id) references Recipes(id)      -- added this line, but not sure if necessary, will just check if the id exists in recipes
);

create table Starred_Recipes (
    recipe_id       integer      not null,
    contains        integer     not null,   -- contains is profile_id
    primary key (recipe_id, contains),
    foreign key (contains) references Profiles(profile_id),
    foreign key (recipe_id) references Recipes(id)      -- added this line, but not sure if necessary, will just check if the id exists in recipes
);


create table Comments (
    comment_id      serial      primary key,
    comment         text        not null,       -- comment being added cant be nothing
    has             integer     not null,      -- = recipes.id
    foreign key (has) references Recipes(id)


);


create table Likes (
    number_of_likes integer     not null,       
    has             integer     not null,      -- = recipes.id
    foreign key (has) references Recipes(id)
);



