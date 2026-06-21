# ai-automation-skills

35 production-tested Claude skills for automation, Gemini cost control, OSS bounty hunting, artifact capture, and ML strategy validation. Distilled from 8 months of indie-hacker work.

> 🧰 **Coming soon:** *Trawlkit* — a paid starter kit that wires these skills into runnable scrape → AI → alert bots in one install. Every skill below ends with a `→ Build the full runnable bot with Trawlkit` pointer. Follow [@barobaonguyen](https://x.com/barobaonguyen) for the launch.

```text
/plugin marketplace add baronguyen001/ai-automation-skills
/plugin install ai-automation-skills@baronguyen001
```

![Skills](https://img.shields.io/badge/skills-35-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Last commit](https://img.shields.io/github/last-commit/baronguyen001/ai-automation-skills) ![Stars](https://img.shields.io/github/stars/baronguyen001/ai-automation-skills)

Demo captures are intentionally not fabricated. The needed screenshots are tracked in [screenshots/README.md](screenshots/README.md).

## Install

Run these inside Claude Code:

```text
/plugin marketplace add baronguyen001/ai-automation-skills
/plugin install ai-automation-skills@baronguyen001
```

Then confirm:

```text
/plugin list
```

Installed skills appear under the `ai-automation-skills:<skill>` namespace.

## What's In The Box

### Automation

| Skill | What it does | Trigger |
|---|---|---|
| `telegram-alerter` | Sends Telegram alerts from Python with env-only credentials, HTML formatting, inline buttons, photo support, and 429 retry handling. | "send a telegram alert", "notify telegram" |
| `slack-webhook-alerter` | Posts run results to a Slack incoming webhook as a Block Kit message with a green/red/yellow status attachment, env-only webhook, no Slack SDK. | "send a slack alert", "post to a slack channel" |
| `cron-dispatch` | Schedules any script on Windows Task Scheduler or Linux cron with logging and an overlap guard. | "run nightly", "set up a cron job" |
| `pipeline-orchestrator` | Chains scrape → AI → alert stages with per-stage retry and a JSON checkpoint so a crashed run resumes. | "chain these steps", "resumable pipeline" |
| `gmail-imap-digest` | Pulls email over IMAP, keeps only allowlisted senders, and renders a daily digest (BYO app-password). | "build a daily email digest", "IMAP fetch" |
| `discord-bot-poller` | Polls one Discord channel for new messages with a bot token from env and dispatches a handler while honoring REST rate limits. | "poll a Discord channel", "watch messages" |
| `webhook-receiver` | A stdlib HTTP receiver that verifies an HMAC signature in constant time and queues each payload to disk for a worker. | "receive a webhook", "verify a webhook signature" |
| `sqlite-state` | Gives scheduled scripts memory between runs: a seen-set for dedup, a cursor to resume, all in one SQLite file. | "dedup across runs", "remember the last id" |
| `notion-row-writer` | Upserts a Notion database row by a stable key with API key and database id from env. | "write to Notion", "upsert by URL" |

### Gemini Meta

| Skill | What it does | Trigger |
|---|---|---|
| `gemini-cost-tracker` | Logs Gemini token usage and estimated USD cost per call, model, and session. | "track gemini cost", "gemini token usage" |
| `gemini-structured-output` | Gets validated JSON from Gemini with Pydantic response schemas and a JSON salvage parser. | "gemini structured output", "responseSchema" |
| `gemini-prompt-cache` | Caches a long, stable system-prompt prefix once so repeated input tokens bill at the cheaper cached rate. | "cache gemini system prompt", "context caching" |
| `gemini-flash-budget` | Runs Flash with `thinking_budget=0` for cheap, fast, high-volume extraction and classification. | "cheaper gemini calls", "disable thinking" |
| `gemini-vision-extract` | Extracts typed JSON from an image (receipt/invoice/screenshot) with Gemini, constrained to a Pydantic schema. | "read a receipt", "image to JSON with gemini" |

### Bounty/Scraping

| Skill | What it does | Trigger |
|---|---|---|
| `algora-bounty-scout` | Scouts public Algora org boards, parses bounty links, dedupes, and filters time-wasters before coding. | "scout algora", "find OSS bounties" |
| `github-label-scout` | Scans a public repo for open issues by label and skips assigned ones, using the token-free public API. | "find issues by label", "good first issue" |
| `pr-body-formatter` | Builds a complete GitHub PR body from a diff summary and issue reference without TODO placeholders. | "write a PR description", "pr body template" |
| `proxy-rotator` | Rotates a pool of HTTP/SOCKS proxies round-robin with failure tracking and a cooldown for dead ones (BYO list). | "rotate proxies", "avoid IP bans" |
| `playwright-login-session` | Captures a Playwright `storage_state` once, then reuses it headless so later runs start already signed in. | "reuse a logged-in session", "skip login each run" |
| `playwright-pdf-snapshot` | Renders any URL to a headless PDF or PNG snapshot with Playwright and no committed cookies. | "save page as PDF", "capture PNG snapshot" |

### Validation

| Skill | What it does | Trigger |
|---|---|---|
| `walk-forward-runner` | Sets up leakage-free rolling time-series validation and flags overfit parameter rankings. | "walk forward validation", "time series cross validation" |
| `backtest-comparator` | Compares strategy variants across years/folds and flags the ones that overfit a single lucky period. | "compare backtest variants", "flag overfit" |
| `config-audit-checklist` | Audits config drift between a snapshot doc, `.env`, and README defaults before a backtest or deploy. | "config audit", "params drift" |

### Infrastructure

| Skill | What it does | Trigger |
|---|---|---|
| `http-retry-session` | A hardened `requests.Session` with urllib3 retry, exponential backoff, a 429/5xx status-forcelist, honored Retry-After, and a default connect/read timeout on every call. | "add retries to my requests", "set request timeouts" |
| `rate-limit-budget` | A token-bucket pacer that smooths bursts to a per-second rate and stops the run at a hard per-run call/credit budget so a free-tier quota survives. | "rate-limit api calls", "stay under the quota" |
| `csv-report-writer` | Turns a run's result rows into a schema'd CSV plus a Markdown table from one column spec, with stable ordering and safe escaping, no pandas. | "export a CSV report", "make a markdown table" |
| `env-config-loader` | Loads a `.env`, validates required keys are present, and reads typed values (int/bool/float/list) with clear errors, stdlib only, no pydantic. | "load my .env", "fail fast on missing env vars" |
| `s3-uploader` | Uploads and downloads run artifacts to S3-compatible storage with bucket and credentials from env. | "upload to S3", "archive artifacts" |
| `pdf-text-extract` | Extracts text and rough table rows from digital PDFs for downstream AI, with no OCR binary required. | "extract PDF text", "pull tables from PDF" |

### Content

| Skill | What it does | Trigger |
|---|---|---|
| `shortform-script` | Drafts short-form or long-form video scripts from a topic plus a creator persona file, using fact slots to avoid invented personal claims. | "write a video script", "tiktok script" |
| `rss-feed-reader` | Parses RSS 2.0 and Atom feeds into one normalized item shape, stdlib only, no feedparser. | "read an RSS feed", "poll a blog feed" |
| `json-schema-validator` | Validates a payload against a JSON Schema subset with readable errors, no jsonschema dependency. | "validate this payload", "reject malformed records" |
| `html-to-text` | Strips HTML to clean text (drops script/style, collapses whitespace) with the standard library only. | "get text out of HTML", "clean scraped HTML" |
| `jsonl-store` | Appends records to JSON Lines with streaming reads and key dedup for durable between-run state. | "log to JSONL", "dedup by id across runs" |
| `url-canonicalizer` | Normalizes URLs (strip tracking params/fragment, sort query) so the same page dedupes to one key. | "dedup links", "normalize scraped URLs" |

## Why These 35

Every skill maps to a real pattern used repeatedly across automation, Gemini, validation, and open-source contribution workflows. The point is not a huge catalog; it is a compact set of skills with concrete examples, reusable assets, and enough install structure to work as a Claude Code plugin marketplace. Each one teaches the reusable technique; *Trawlkit* (coming soon) wires them into a full runnable bot.

## 30-Second Example

Trigger:

```text
Track Gemini cost for this batch ranking script.
```

Claude can wrap calls with `gemini-cost-tracker`:

```python
tracker.record("gemini-2.5-flash", resp.usage_metadata)
print(tracker.summary())
```

Example output:

```text
Calls: 3 | Total: $0.001242
  gemini-2.5-flash-lite: $0.000180
  gemini-2.5-flash: $0.001062
```

## Design

See [docs/design_principles.md](docs/design_principles.md). The short version: one concrete example per skill, no `<your value here>` placeholders, no private production parameters, and no secrets.

## Contributing

See [docs/contributing.md](docs/contributing.md) for the frontmatter rules, validation command, and local `claude plugin validate .` check.

## License

MIT. See [LICENSE](LICENSE).

## Star History

Add the Star History chart after the repo has enough public signal to make the chart useful. Until then, this section stays as a placeholder.
