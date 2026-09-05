# Changelog

## [0.1.1] - 2026-03-10
- Adjusted GitHub Actions daily schedule from `02:00 UTC` to `02:07 UTC` (`10:07` Beijing time) to reduce top-of-hour scheduler contention risk.
- Added `timeout-minutes: 45` for the daily pipeline job to avoid indefinite hangs.
- Synced deployment documentation with the updated schedule.

## [0.1.0] - 2026-03-09
- Initial release with source registry, crawler pipeline, daily diff, exports, website, CI workflows, docs, and tests.
