with products(product_name) as (
    select 'All-Access Membership - 1 Month Renewal' union all
    select 'All-Access Membership Upgrade - 1 Month Recurring' union all
    select 'All-Access Membership Upgrade - 1 Month Recurring Holiday Pricing' union all
    select 'MyTV.TaiSeng Subscription - 1 Month Recurring' union all
    select 'All-Access Membership - 1 Month Renewal Holiday Pricing' union all
    select 'All-Access Membership - 1 Month (Mail)' union all
    select 'Drama Membership - 1 Month Renewal' union all
    select 'Drama Membership - 1 Month (Mail)' union all
    select 'Anime Membership - 1 Month Renewal' union all
    select 'Drama Membership - 1 Month Recurring' union all
    select 'Anime Membership - 1 Month (Mail)' union all
    select 'MyTV.TaiSeng Subscription - 1 Month Renewal' union all
    select 'Drama Membership - 1 Month Recurring (iTunes App Store)' union all
    select 'MyTV.TaiSeng DTV Promo - 1 Month Renewal' union all
    select 'MyTV.TaiSeng Special Offer - 1 Month Renewal' union all
    select 'All-Access Membership - 1 Month Recurring (iTunes App Store)' union all
    select 'Anime Membership - 1 Month Recurring (iTunes App Store)' union all
    select 'Manga Membership - 1 Month Renewal' union all
    select 'Manga Membership - 1 Month Recurring' union all
    select 'Super Fan Pack - 1 Month Recurring (iTunes)' union all
    select 'Super Fan Pack - 1 Month Recurring' union all
    select 'Fan Pack - 1 Month Recurring' union all
    select 'Fan Pack - 1 Month Recurring (iTunes)'
),

subscriptions as (
    select *
    from cr_warehouse.cr_fact_subscription_history as h
    inner join products as p on h.product_name = p.product_name
    where subscription_created_date >= '2017-07-01' -- and '2017-12-31'
    and country_code in ('US', 'MX')
)
select
    country_code as country,
    datediff('months', '2017-07-01', subscription_created_date) as month,
    floor(months_between(LEAST(subscription_product_end_date, GETDATE()::date), subscription_created_date)) as tenure,
    count(*)
from subscriptions
group by 1, 2, 3
order by 1, 2, 3
