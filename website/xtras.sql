create or replace view newsfeeds(id, name, description, photo, serving, creates, creator, contains, likes, dislikes, display_name, creation_time, creation_date)
as
    select r.id, name, description, photo, serving, creates, creator, contains, num_of_likes, num_of_dislikes, display_name, creation_time, creation_date
    from recipes r
        join subscribed s on (r.creates = s.subscribed_id)
        join profiles p on (r.creates = p.profile_id)
;





create view profile_subs as
Select p.profile_id, p.first_name, p.last_name, p.display_name, p.profile_pic, p.bio, p.custom_url, p.sub_count, p.recipe_count, s.subscriber_id, s.contains
From
    profiles as p
    LEFT JOIN subscriber as s on p.profile_id = s.subscriber_id;






create view profile_subbed as
Select p.profile_id, p.first_name, p.last_name, p.display_name, p.profile_pic, p.bio, p.custom_url, p.sub_count, p.recipe_count, s.subscribed_id, s.contains
From
    profiles as p
    LEFT JOIN subscribed as s on p.profile_id = s.subscribed_id;

