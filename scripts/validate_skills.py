from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "telegram-alerter",
    "gemini-cost-tracker",
    "gemini-structured-output",
    "walk-forward-runner",
    "config-audit-checklist",
    "algora-bounty-scout",
    "pr-body-formatter",
    "shortform-script",
    "cron-dispatch",
    "pipeline-orchestrator",
    "gmail-imap-digest",
    "gemini-prompt-cache",
    "gemini-flash-budget",
    "github-label-scout",
    "backtest-comparator",
    "webhook-receiver",
    "sqlite-state",
    "proxy-rotator",
    "gemini-vision-extract",
    "playwright-login-session",
    "slack-webhook-alerter",
    "http-retry-session",
    "csv-report-writer",
    "env-config-loader",
    "rate-limit-budget",
    "s3-uploader",
    "pdf-text-extract",
    "discord-bot-poller",
    "notion-row-writer",
    "playwright-pdf-snapshot",
    "rss-feed-reader",
    "json-schema-validator",
    "html-to-text",
    "jsonl-store",
    "url-canonicalizer",
}
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "version",
    "when_to_use",
    "argument-hint",
    "allowed-tools",
    "disallowed-tools",
    "disable-model-invocation",
    "user-invocable",
    "model",
    "effort",
    "context",
    "agent",
    "paths",
    "arguments",
    "hooks",
    "shell",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")


def parse_frontmatter(text: str, path: Path) -> dict[str, Any]:
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} is missing YAML frontmatter")

    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"{path.relative_to(ROOT)} has an unterminated frontmatter block")

    raw = text[4:end]
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(raw) or {}
    except Exception:
        data = {}
        for line in raw.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if ":" not in line:
                fail(f"{path.relative_to(ROOT)} has unsupported frontmatter line: {line}")
            key, value = line.split(":", 1)
            value = value.strip()
            if (
                len(value) >= 2
                and value[0] == value[-1]
                and value[0] in {"'", '"'}
            ):
                value = value[1:-1]
            data[key.strip()] = value

    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} frontmatter must be a mapping")

    return data


def tracked_files() -> list[Path]:
    try:
        proc = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        return [ROOT / line for line in proc.stdout.splitlines() if line.strip()]
    except Exception:
        return [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]


def validate_manifests() -> None:
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    plugin = load_json(ROOT / ".claude-plugin" / "plugin.json")

    if not marketplace.get("name"):
        fail("marketplace.json must have name")
    if not marketplace.get("owner", {}).get("name"):
        fail("marketplace.json must have owner.name")
    if not marketplace.get("plugins"):
        fail("marketplace.json must have non-empty plugins")
    if not plugin.get("name"):
        fail("plugin.json must have name")
    if plugin.get("version") != "0.6.0":
        fail("plugin.json version must be 0.6.0")


def validate_skills() -> None:
    skill_root = ROOT / "skills"
    found = {path.name for path in skill_root.iterdir() if path.is_dir()}
    if found != EXPECTED_SKILLS:
        fail(f"skill folders mismatch: expected {sorted(EXPECTED_SKILLS)}, found {sorted(found)}")

    kebab = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    for folder in sorted(skill_root.iterdir()):
        if not folder.is_dir():
            continue
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            fail(f"{folder.relative_to(ROOT)} is missing SKILL.md")

        text = skill_md.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text, skill_md)
        unknown = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
        if unknown:
            fail(f"{skill_md.relative_to(ROOT)} has undocumented frontmatter keys: {sorted(unknown)}")

        name = frontmatter.get("name")
        if name:
            if not isinstance(name, str) or not kebab.fullmatch(name):
                fail(f"{skill_md.relative_to(ROOT)} name must be kebab-case")
            if name != folder.name:
                fail(f"{skill_md.relative_to(ROOT)} name must match its folder")

        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            fail(f"{skill_md.relative_to(ROOT)} needs a non-empty description")
        if len(description) > 1536:
            fail(f"{skill_md.relative_to(ROOT)} description is too long")

        if "\n## Concrete example\n" not in text:
            fail(f"{skill_md.relative_to(ROOT)} needs a ## Concrete example section")

    for path in skill_root.rglob("assets/*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            fail(f"{path.relative_to(ROOT)} is not valid Python: {exc}")


def secret_patterns() -> list[re.Pattern[str]]:
    return [
        re.compile("AIza" + r"[0-9A-Za-z_-]{30,}"),
        re.compile("sk-" + r"[A-Za-z0-9]{20,}"),
        re.compile("ghp_" + r"[A-Za-z0-9]{30,}"),
        re.compile("github" + r"_pat_"),
        re.compile(r"[0-9]{8,}:AA" + r"[A-Za-z0-9_-]{30,}"),
        re.compile("xoxb" + r"-"),
    ]


def scan_for_secrets() -> None:
    patterns = secret_patterns()
    for path in tracked_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in patterns:
            if pattern.search(text):
                fail(f"potential secret pattern found in {path.relative_to(ROOT)}")


def validate_readme_length() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    words = re.findall(r"\b[\w'-]+\b", readme)
    if len(words) > 1500:
        fail(f"README.md has {len(words)} words; expected <= 1500")


def main() -> None:
    validate_manifests()
    validate_skills()
    scan_for_secrets()
    validate_readme_length()
    print("OK: manifests, skills, Python assets, README length, and secret scan passed")


if __name__ == "__main__":
    main()
