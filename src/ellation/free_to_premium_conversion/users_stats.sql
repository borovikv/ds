with subscriptions as (
    select
        a.dwed_account_key,
        a.account_created,
        min(s.activation_date) as subscription_date
    from etp_warehouse.dim_account as a
    left join spectrum.cr_premium_memberships as s on a.account_id = s.user_id and a.dwed_tenant_key = 2 -- CR
    where s.payment_status = 2 -- PAID
        and a.country_code='US'
    group by 1, 2
)
select
    abs(ceil(months_between(subscription_date, account_created))) as months,
    count(*)
from subscriptions
group by 1
