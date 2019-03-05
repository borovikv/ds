with weeks_secconds as (
select
    fd.dwed_account_key,
    case when cr.subscription_product_end_date < cr.subscription_created_date + 105 then 1 else 0 end as churn,
    floor(datediff(day,  cr.subscription_created_date, dd.calendar_date) / 7) as week_no,
    case when dd.calendar_date <= dm.media_air_date + 7 then 'paid' else 'free' end as content_type,
    sum(fd.daily_seconds_viewed) as seconds
from
    etp_warehouse.fact_daily_media_viewership as fd
    join etp_warehouse.dim_date dd on fd.dwed_video_watched_date_key = dd.dwed_date_key
    join cr_warehouse.cr_fact_subscription_history as cr on fd.dwed_account_key = cr.account_key
    join etp_warehouse.dim_media as dm on dm.dwed_media_key = fd.dwed_media_key
where
    cr.subscription_created_date between '2018-07-30' and '2018-08-12'
    and cr.product_name in ('All-Access Membership - 1 Month Renewal', 'All-Access Membership Upgrade - 1 Month Recurring', 'All-Access Membership Upgrade - 1 Month Recurring Holiday Pricing', 'MyTV.TaiSeng Subscription - 1 Month Recurring', 'All-Access Membership - 1 Month Renewal Holiday Pricing', 'All-Access Membership - 1 Month (Mail)', 'Drama Membership - 1 Month Renewal', 'Drama Membership - 1 Month (Mail)', 'Anime Membership - 1 Month Renewal', 'Drama Membership - 1 Month Recurring', 'Anime Membership - 1 Month (Mail)', 'MyTV.TaiSeng Subscription - 1 Month Renewal', 'Drama Membership - 1 Month Recurring (iTunes App Store)', 'MyTV.TaiSeng DTV Promo - 1 Month Renewal', 'MyTV.TaiSeng Special Offer - 1 Month Renewal', 'All-Access Membership - 1 Month Recurring (iTunes App Store)', 'Anime Membership - 1 Month Recurring (iTunes App Store)', 'Manga Membership - 1 Month Renewal', 'Manga Membership - 1 Month Recurring', 'Super Fan Pack - 1 Month Recurring (iTunes)', 'Super Fan Pack - 1 Month Recurring', 'Fan Pack - 1 Month Recurring', 'Fan Pack - 1 Month Recurring (iTunes)')
    and cr.country_code='US'
    and cr.cancellation_reason in ('ACTIVE_SUBSCRIPTION', 'USER_CANCELLED')
    and cr.subscription_product_end_date > cr.subscription_created_date + 7*12 - 1
    and dd.calendar_date between cr.subscription_created_date and cr.subscription_created_date + 7*12 - 1
group by 1,2,3,4
)
select * from weeks_secconds
