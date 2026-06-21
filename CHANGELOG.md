# Changelog

## v0.6.0 — 2026-06-21

- Grew the catalog from 30 to 35 skills. Added 5 new stdlib-only skills:
  - `rss-feed-reader` — parse RSS 2.0 and Atom feeds into one normalized item shape (no feedparser).
  - `json-schema-validator` — validate a payload against a JSON Schema subset with readable errors (no jsonschema dependency).
  - `html-to-text` — strip HTML to clean plain text, dropping script/style and collapsing whitespace (no BeautifulSoup/lxml).
  - `jsonl-store` — durable append-only JSON Lines state with streaming reads and key-based dedup across runs.
  - `url-canonicalizer` — normalize URLs (strip tracking params + fragment, sort query) so the same page dedupes to one key.
- Bumped plugin/marketplace to v0.6.0 and updated the skill table and validator's expected set.

## v0.5.0 — 2026-06-11

- Grew the catalog from 25 to 30 skills. Added 5 new skills:
  - `s3-uploader` — upload/download run artifacts to S3-compatible storage with BYO bucket, endpoint, and credentials from env; supports generic object storage without committed credentials.
  - `pdf-text-extract` — extract digital PDF text plus rough table rows for downstream AI using pure-Python PDF libraries when available, with no OCR binary requirement.
  - `discord-bot-poller` — poll one Discord channel for new messages with a bot token from env, dispatch a handler oldest-to-newest, and honor REST rate limits.
  - `notion-row-writer` — upsert a Notion database row by a stable key using `NOTION_API_KEY` and database id from env, with clear missing-config errors.
  - `playwright-pdf-snapshot` — render any URL to headless PDF and/or PNG snapshots with Playwright, no committed cookies or credentials.
- Bumped plugin + marketplace version to `0.5.0`; updated the validator's expected skill set and README count.

## v0.4.0 — 2026-06-10

- Grew the catalog from 20 to 25 skills. Added 5 new skills:
  - `slack-webhook-alerter` — post a run result to a Slack incoming webhook as a Block Kit message wrapped in a green/red/yellow status attachment, with the webhook URL read from env only and no Slack SDK (mirrors `telegram-alerter` so a run can fan out to both).
  - `http-retry-session` — a hardened `requests.Session` with a urllib3 `Retry` policy (exponential backoff, a 429/5xx status-forcelist, honored `Retry-After`) and a `TimeoutSession` that injects a default `(connect, read)` timeout into every call so no request hangs.
  - `csv-report-writer` — turn a run's list of result rows into a schema'd CSV and a Markdown table from one column spec, with stable ordering, CSV quoting, and pipe/newline escaping for Markdown; stdlib only, no pandas.
  - `env-config-loader` — load a `.env`, validate that required keys are present (one clear error listing every missing key), and read typed values (`get_int`/`get_bool`/`get_float`/`get_list`) with readable errors; stdlib only, no python-dotenv, no pydantic.
  - `rate-limit-budget` — a token-bucket pacer that smooths bursts to a per-second rate and stops the run at a hard per-run call/cost budget so a free-tier quota survives; cross-links the `helius-rate-limiter` repo for the production library.
- Each new skill ships a runnable `assets/*.py` helper with an offline `__main__` self-test, plus the `→ Build the full runnable bot with Trawlkit` footer.
- Bumped plugin + marketplace version to `0.4.0`; updated the validator's expected skill set and version gate.

## v0.3.0 — 2026-06-06

- Grew the catalog from 15 to 20 skills. Added 5 new skills:
  - `webhook-receiver` — a tiny stdlib HTTP server that verifies an HMAC signature in constant time and queues each payload to disk for a worker to drain (no web framework).
  - `sqlite-state` — durable run-state between scheduled runs over one SQLite file: a seen-set for dedup, a key/value cursor to resume, and order-preserving new-item filtering.
  - `proxy-rotator` — rotate a pool of HTTP/SOCKS proxies round-robin with failure tracking and a cooldown that benches dead proxies (BYO list via env; none shipped).
  - `gemini-vision-extract` — structured extraction from an image with Gemini, constrained to a Pydantic `response_schema` so the result is typed JSON, not prose.
  - `playwright-login-session` — capture a `storage_state` once via manual login, then reuse it headless so later runs start already signed in (no committed cookies).
- Fixed the stale `barobaonguyen` GitHub namespace (the account was renamed to `baronguyen001`; GitHub only redirected): manifests, plugin homepage/repository/author, install commands, README badges, and LICENSE now point at `baronguyen001`. The marketplace install is now `/plugin install ai-automation-skills@baronguyen001`. (The `x.com/barobaonguyen` handle is unchanged — it is still the live X account.)
- Bumped plugin + marketplace version to `0.3.0`; updated the validator's expected skill set and version gate.

## v0.2.0 — 2026-06-03

- Grew the catalog from 8 to 15 skills. Added 7 new skills:
  - `cron-dispatch` — schedule any script on Windows Task Scheduler or Linux cron, with logging and an overlap guard.
  - `pipeline-orchestrator` — chain scrape → AI → alert stages with per-stage retry and a JSON checkpoint for resumable runs.
  - `gmail-imap-digest` — pull email over IMAP into a daily digest, filtered to an allowlist of trusted sender domains (BYO app-password).
  - `gemini-prompt-cache` — cache a long, stable system-prompt prefix so repeated input tokens bill at the cheaper cached rate.
  - `gemini-flash-budget` — Flash with `thinking_budget=0` for cheap, fast, high-volume extraction and classification.
  - `github-label-scout` — scan a public repo for open issues by label and skip assigned ones, via the token-free public API.
  - `backtest-comparator` — compare strategy variants across years/folds and flag the ones that overfit a single lucky period.
- New skills carry a `version` frontmatter field and a `→ Build the full runnable bot with Trawlkit` footer pointer.
- Bumped plugin + marketplace version to `0.2.0`; updated the validator's expected skill set and allowed frontmatter keys.

## v0.1.1 — 2026-05-29

- Renamed repo + plugin to `ai-automation-skills` (keyword-first for global SEO; GitHub redirects the old URL). Marketplace namespace is now `barobaonguyen` → install with `/plugin install ai-automation-skills@barobaonguyen`.

## v0.1.0 — 2026-05-29

- Shipped the first public `barobao-skills` marketplace release.
- Added 8 Claude Code skills: `telegram-alerter`, `gemini-cost-tracker`, `gemini-structured-output`, `walk-forward-runner`, `config-audit-checklist`, `algora-bounty-scout`, `pr-body-formatter`, and `shortform-script`.
- Added marketplace/plugin manifests, validation script, CI workflow, install docs, design principles, and screenshot capture checklist.
