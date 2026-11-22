# Data Dictionary

## `content.csv`
One row per supplied Instagram feed post or YouTube top-content record.

| Field | Meaning |
|---|---|
| `platform` | Instagram or YouTube |
| `content_id` | Stable local ID; YouTube video IDs are native IDs. Instagram IDs are generated local keys because native IDs were not present in the audit table. |
| `content_type` | Reel, Carousel, Short or Long-form |
| `publish_date` | Publication date; blank where source did not provide it. |
| `title_or_topic` | Exact YouTube title or audit-provided Instagram descriptive label/paraphrase. |
| `views` | Content-level views as reported. |
| `reach` | Instagram per-content accounts reached; not supplied for YouTube shortlist. |
| `impressions` | Content-level impressions; missing where not supplied. |
| `likes`, `comments`, `shares`, `saves`, `reposts` | Per-content interaction counts, missing when not supplied. |
| `interactions` | Audit-provided interaction aggregate for Instagram rows; not provided for YouTube shortlist. |
| `follows_or_subs_net` | Instagram follows attributed to the post or YouTube net subscribers attributed to the video; metric names differ by platform. |
| `initial_plays`, `replays` | Instagram Reel metrics. |
| `watch_time_seconds` | Instagram post-level seconds or YouTube watch hours converted to seconds from the supplied report. |
| `avg_watch_time_seconds` | Instagram average watch time where supplied. |
| `skip_rate_pct` | Instagram Reel skip rate where supplied, stored as percentage points (e.g. 49.5 means 49.5%). |
| `follower_views_pct` | Instagram follower-view percentage where supplied, stored as percentage points. |
| `engagement_rate_reach_pct`, `engagement_rate_views_pct` | Audit-calculated Instagram rates, stored as percentage points. |
| `engaged_views` | Not supplied at individual content level in the current audit. |
| `source_detail` | Source category/provenance. |
| `data_completeness` | Completeness qualification. |
| `notes` | Caveats. |

## Other datasets

- `stories.csv`: Instagram archived Story rows; includes views, reach, impressions, Story likes, interactions, navigation, profile visits, follower and non-follower views.
- `daily_metrics.csv`: Instagram account-level daily figures. The Views metric is aggregated IG + FB cross-posted content according to the audit.
- `traffic_sources.csv`: YouTube lifetime traffic-source aggregate table.
- `format_summary.csv`: Platform format aggregates. Do not combine rows across platforms as if metric definitions were identical.
- `platform_summary.csv`: Long-form metric/value table with reporting period and source notes.
- `audience_activity.csv`: Top two reported hours by weekday in America/Los_Angeles timezone; not a full hourly grid.
- `data_quality_issues.csv`: Known conflicts, omissions and coverage limitations.

## Missing-value policy
Source values such as “No figure”, “Unavailable” or “Not returned” are stored as null/blank. A blank value does not mean zero.
