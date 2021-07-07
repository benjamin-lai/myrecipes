create or replace view newsfeeds(id, name, description, photo, serving, creates, creator, contains, likes, dislikes, display_name, creation_time, creation_date)
as
    select r.id, name, description, photo, serving, creates, creator, contains, num_of_likes, num_of_dislikes, display_name, creation_time, creation_date
    from recipes r
        join subscribed_to_lists s on (r.creates = s.subscribed_id)
        join profiles p on (r.creates = p.profile_id)
;