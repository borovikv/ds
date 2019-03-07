with subscriptions as (
    select
        a.dwed_account_key,
        a.account_created,
        min(s.activation_date)
    from etp_warehouse.dim_account as a
    inner join spectrum.cr_premium_memberships as s on a.account_id = s.user_id and a.dwed_tenant_key = 2 -- CR
    where s.payment_status = 2 -- PAID
        and a.account_created >= '2018-01-01' and '2018-05-31'
        and a.country_code='US'
    group by 1, 2
),
media as(
    select
        top_level_media_id,
        count(media_id) as num_episodes
    from etp_warehouse.dim_media
    where dwed_tenant_key=2
    group by 1
),
users as (
    select
        distinct(dwed_account_key),
        dense_rank() over(order by account_key desc) as userIdInt
    from subscriptions
),
user_viewerships as (
    select
        cr.account_key,
        dm.media_id,
        dm.top_level_media_id,
        dm.media_duration,
        max(COALESCE(fd.video_end_watch_dtm, fd.dwmd_created_ts)) as max_date,
        case when sum(fd.daily_seconds_viewed)/dm.media_duration < 1.0
            then sum(fd.daily_seconds_viewed)/dm.media_duration
            else 1.0
        end as FracViewed,
        case when sum(fd.daily_seconds_viewed)>=dm.media_duration*0.8
                or (sum(fd.daily_seconds_viewed)>=dm.media_duration*0.3
                    and max(fd.daily_max_playhead_seconds) >= dm.media_duration*0.8)
            then 1
            else 0
        end as episode_watched
    from
        etp_warehouse.fact_daily_media_viewership as fd
        join subscriptions as cr on fd.dwed_account_key = cr.account_key
        join etp_warehouse.dim_media as dm on dm.dwed_media_key=fd.dwed_media_key
    where dm.media_duration > 0
    group by 1,2,3,4
)
select
    u.userIdInt,
    b.account_key,
    b.top_level_media_id,
    m.num_episodes,
    max(b.max_date),
    case when sum(b.episode_watched)= m.num_episodes then True else False end as isCompletelyWatched,
    case when avg(m.num_episodes) > 0 then sum(b.FracViewed)/avg(m.num_episodes) else 0 end as avgFracViewed -- our 1.1433518609513964 need 0.9625961
from user_viewerships as b
inner join media as m on m.top_level_media_id = b.top_level_media_id
inner join users as u on u.account_key = b.account_key
group by 1,2,3,4
