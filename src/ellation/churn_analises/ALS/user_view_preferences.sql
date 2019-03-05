with subscription_users as(
    select
        cr.account_key,
        cr.subscription_created_date,
        cr.subscription_created_date + 7*5 - 1 as research_period_end_date,
        case when cr.subscription_product_end_date < cr.subscription_created_date+45 then 1 else 0 end as churn
    from 
        cr_warehouse.cr_fact_subscription_history as cr
    where
        cr.subscription_created_date between '2018-01-01' and '2018-12-31'
        and cr.product_name in (
            'All-Access Membership - 1 Month Renewal',
            'All-Access Membership Upgrade - 1 Month Recurring',
            'All-Access Membership Upgrade - 1 Month Recurring Holiday Pricing',
            'MyTV.TaiSeng Subscription - 1 Month Recurring',
            'All-Access Membership - 1 Month Renewal Holiday Pricing',
            'All-Access Membership - 1 Month (Mail)',
            'Drama Membership - 1 Month Renewal',
            'Drama Membership - 1 Month (Mail)',
            'Anime Membership - 1 Month Renewal',
            'Drama Membership - 1 Month Recurring',
            'Anime Membership - 1 Month (Mail)',
            'MyTV.TaiSeng Subscription - 1 Month Renewal',
            'Drama Membership - 1 Month Recurring (iTunes App Store)',
            'MyTV.TaiSeng DTV Promo - 1 Month Renewal',
            'MyTV.TaiSeng Special Offer - 1 Month Renewal',
            'All-Access Membership - 1 Month Recurring (iTunes App Store)',
            'Anime Membership - 1 Month Recurring (iTunes App Store)',
            'Manga Membership - 1 Month Renewal',
            'Manga Membership - 1 Month Recurring',
            'Super Fan Pack - 1 Month Recurring (iTunes)',
            'Super Fan Pack - 1 Month Recurring',
            'Fan Pack - 1 Month Recurring',
            'Fan Pack - 1 Month Recurring (iTunes)'
        )
        and cr.country_code='US' 
        and cr.cancellation_reason in ('ACTIVE_SUBSCRIPTION', 'USER_CANCELLED')
        and cr.subscription_product_end_date > cr.subscription_created_date + 7*5 - 1
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
        distinct(account_key),
        dense_rank() over(order by account_key desc) as userIdInt
    from subscription_users
),
by_episodes as (
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
        join subscription_users as cr on fd.dwed_account_key = cr.account_key
        join etp_warehouse.dim_media as dm on dm.dwed_media_key=fd.dwed_media_key
    where dm.media_duration>0
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
from by_episodes as b
    join media as m on m.top_level_media_id = b.top_level_media_id
    join users as u on u.account_key = b.account_key
group by 1,2,3,4
