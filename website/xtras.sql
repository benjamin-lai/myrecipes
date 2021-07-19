create or replace view newsfeeds(id, name, description, photo, serving, creates, creator, contains, likes, dislikes, display_name, creation_time, creation_date)
as
    select r.id, name, description, photo, serving, creates, creator, contains, num_of_likes, num_of_dislikes, display_name, creation_time, creation_date
    from recipes r
        join subscribed s on (r.creates = s.subscribed_id)
        join profiles p on (r.creates = p.profile_id)
;

'''
create or replace view profiles_detailed(profile_id, first_name, last_name, display_name, profile_pic, temp_pic, bio, custom_url, owns)
as
    select profile_id, first_name, last_name, display_name, profile_pic, temp_pic, bio, custom_url, owns
    from profiles p
        join Subscribed s on (p.profile_id = s.subscribed_id)
        join users u on (p.profile_id = u.id)
        join Subscriber s2 on (p.profile_id = s2.contains)
        join recipes r on (p.profile_id = r.creates)
;

create or replace view profile_recipes(profile_id, first_name, last_name, display_name, profile_pic, temp_pic, bio, custom_url, owns)
as
    select profile_id, first_name, last_name, display_name, profile_pic, temp_pic, bio, custom_url, owns
    from profiles p
        join users u on (p.profile_id = u.id)
        join recipes r on (p.profile_id = r.creates)
;

create or replace view newsfeeds(id, name, description, photo, serving, creates, creator, contains, likes, dislikes, display_name)
as
    select r.id, name, description, photo, serving, creates, creator, contains, num_of_likes, num_of_dislikes, display_name
    from recipes r
        join Subscribed s on (r.creates = s.subscribed_id)
        join likes l on (l.has = r.id)
        join profiles p on (r.creates = p.profile_id)
;
'''

Create View BULD as
Select t1.shape, t1.polygon_id, t1.name, t1.height, t1.ground_clearance,
       t1.iso_country_code, t2.venue_id, t3.feature_type, t3.main_feature_type
From
    BULD_base as t1
    LEFT JOIN Venue as t2 ON t1.polygon_id = t2.polygon_id 
    LEFT JOIN Feature as t3 ON t1.polygon_id = t3.polygon_id;


create view profile_subs as
Select p.profile_id, p.first_name, p.last_name, p.display_name, p.profile_pic, p.bio, p.custom_url, p.sub_count, p.recipe_count, s.subscriber_id, s.contains
From
    profiles as p
    LEFT JOIN subscriber as s on p.profile_id = s.subscriber_id;

class profiles_subs(db.Model, UserMixin):
    profile_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    display_name = db.Column(db.String(150))
    profile_pic = db.Column(db.String(150))
    custom_url = db.Column(db.String(150), unique=True)
    subscriber_id = db.Column(db.Integer, primary_key=True) #initialise to subscriber's id
    contains = db.Column(db.Integer, primary_key=True) # profile (focus)

ALTER TABLE profiles
ADD COLUMN sub_count integer default 0,
ADD COlumn recipe_count integer default 0;