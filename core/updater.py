"""Notify-only update checks for GitHub Releases."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
import urllib.error
import urllib.request


DEFAULT_RELEASE_REPO = "TomBadash/Mouser"
_GITHUB_API = "https://api.github.com/repos/{repo}/releases/latest"
_USER_AGENT = "Mouser update checker"


@dataclass(frozen=True)
class LatestRelease:
    tag_name: str
    html_url: str
    name: str = ""
    published_at: str = ""


def _normalized_stable_parts(version: str) -> tuple[int, ...] | None:
    value = (version or "").strip()
    if value.startswith("v"):
        value = value[1:]
    if not value or "-" in value:
        return None
    match = re.fullmatch(r"\d+(?:\.\d+)*", value)
    if not match:
        return None
    return tuple(int(part) for part in value.split("."))


def _padded(parts: tuple[int, ...], length: int) -> tuple[int, ...]:
    return parts + (0,) * max(0, length - len(parts))


def is_newer(current: str, latest: str) -> bool:
    """Return True when latest is a newer stable semver-ish version."""
    current_parts = _normalized_stable_parts(current)
    latest_parts = _normalized_stable_parts(latest)
    if current_parts is None or latest_parts is None:
        return False
    length = max(len(current_parts), len(latest_parts))
    return _padded(latest_parts, length) > _padded(current_parts, length)


def fetch_latest_release(
    repo: str = DEFAULT_RELEASE_REPO,
    timeout: float = 5.0,
) -> LatestRelease | None:
    """Fetch the latest GitHub Release metadata.

    This is deliberately notify-only: it fetches release metadata but never
    downloads release assets.
    """
    repo = (repo or "").strip()
    if not repo or "/" not in repo:
        return None
    url = _GITHUB_API.format(repo=repo)
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": _USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if getattr(response, "status", 200) >= 400:
                return None
            payload = json.loads(response.read().decode("utf-8"))
    except (
        OSError,
        TimeoutError,
        urllib.error.URLError,
        json.JSONDecodeError,
        UnicodeDecodeError,
    ):
        return None

    if not isinstance(payload, dict):
        return None
    tag_name = str(payload.get("tag_name") or "").strip()
    html_url = str(payload.get("html_url") or "").strip()
    if not tag_name or not html_url:
        return None
    return LatestRelease(
        tag_name=tag_name,
        html_url=html_url,
        name=str(payload.get("name") or ""),
        published_at=str(payload.get("published_at") or ""),
    )
