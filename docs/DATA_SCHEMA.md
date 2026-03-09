# Data Schema

Fields:
`record_id`, `org_name`, `org_group`, `job_title`, `job_type`, `location`,
`country_or_region`, `deadline`, `posted_date`, `job_url`, `source_url`,
`source_type`, `summary`, `language`, `scraped_at`, `scraped_date_bj`,
`is_new_today`, `last_seen_date`, `status`.

`status` usage:
- `active`: seen in current crawl.
- `not_seen_today`: historical record not seen in current crawl, kept for cumulative tracking.
