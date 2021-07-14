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
    custom_url      text,
    owns            integer     not null,   -- user.id  = profile.id =  owns? may be redundant, just mapping how its shown through 3311
    foreign key (owns) references Users(id) -- or just change owns to profile_id or something as use that as the relation.
);

create table Recipes (
    id              serial      primary key,
    name            text        not null,
    description     text        not null,
    photo           text,
    serving         int         not null,
    num_of_likes    int         default 0,
    num_of_dislikes int         default 0,
    creates         integer     not null,   -- users.id
    creator         text        not null,
    meal_type       text        not null,
    creation_time   time        default DATE_TRUNC('second', localtime),
    creation_date   date        default current_date,
    foreign key (creates) references Users(id)     
);

create table History (
    id                   serial      primary key,
    userid               integer        not null,
    recipe               integer        not null,
    last_view_time       time           default DATE_TRUNC('second', localtime),
    last_view_date       date           default current_date,
    foreign key (userid) references Users(id),
    foreign key (recipe) references Recipes(id)
);

create table Ingredient (
    id              serial      primary key,
    recipe_id integer references Recipes(id),
    ingredient      text,
    dosage          int,
    unit_name       text      
);

create table RecipeStep(
    recipe_id       integer references Recipes(id),
    step_no         int     not null,
    step_comment    text    not null,
    photo           text,
    primary key(recipe_id, step_no)
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
    owns            integer     not null,
    foreign key (has) references Recipes(id),
    foreign key (owns) references Users(id)
    
);


create table Likes (
    id              serial      primary key,
    like_status     integer     not null,           -- 1 for liked, 0 for nothing, -1 for dislike
    has             integer     not null,      -- = recipes.id
    own             integer     not null,
    foreign key (own) references Users(id),
    foreign key (has) references Recipes(id)
);

create table Codes (
    id              serial      primary key,
    reset_code      integer     not null,
    own             integer     not null,
    foreign key (own) references Users(id)
);