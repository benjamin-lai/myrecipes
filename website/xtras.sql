create or replace view newsfeeds(id, name, description, photo, serving, creates, creator, contains, likes, display_name)
as
    select id, name, description, photo, serving, creates, creator, contains, number_of_likes, display_name
    from recipes r
        join subscribed s on (r.creates = s.subscribed_id)
        join likes l on (l.has = r.id)
        join profiles p on (r.creates = p.profile_id)
;