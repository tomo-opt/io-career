from __future__ import annotations

import hashlib
import json
import re
from typing import Dict, Iterable, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dateutil import parser as dt_parser

from io_career.models import JobRecord
from io_career.utils.time_utils import bj_date_str, now_utc


def infer_job_type(text: str) -> str:
    low = (text or "").lower()
    if "intern" in low:
        return "Internship"
    if "trainee" in low or "traineeship" in low:
        return "Traineeship"
    if "young professional" in low:
        return "Young Professionals"
    return "Early Career"


def parse_date_safe(value: str) -> str:
    if not value:
        return ""
    try:
        dt = dt_parser.parse(value, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return value[:20]


def make_record_id(org_name: str, title: str, location: str, job_url: str) -> str:
    seed = "|".join([org_name, title, location, job_url]).encode("utf-8")
    return hashlib.sha1(seed).hexdigest()[:16]


def _nested_value(obj: Dict, key_path: str):
    if not key_path:
        return ""
    value = obj
    for part in str(key_path).split("."):
        if isinstance(value, dict):
            value = value.get(part, "")
        elif isinstance(value, list):
            if part.isdigit():
                idx = int(part)
                if 0 <= idx < len(value):
                    value = value[idx]
                else:
                    return ""
            else:
                return ""
        else:
            return ""
    if isinstance(value, (str, int, float)):
        return str(value)
    return ""


def normalize_item(source: Dict, item: Dict) -> JobRecord:
    title = (item.get("job_title") or "").strip()
    location = (item.get("location") or "").strip()
    fallback_job_url = source.get("job_url_template") or source["source_url"]
    job_url = (item.get("job_url") or fallback_job_url).strip()
    summary = (item.get("summary") or "").strip()
    today_bj = bj_date_str()

    return JobRecord(
        record_id=make_record_id(source["org_name"], title, location, job_url),
        org_name=source["org_name"],
        org_group=source["org_group"],
        job_title=title,
        job_type=item.get("job_type") or infer_job_type(f"{title} {summary}"),
        location=location,
        country_or_region=item.get("country_or_region") or location,
        deadline=parse_date_safe(item.get("deadline") or ""),
        posted_date=parse_date_safe(item.get("posted_date") or ""),
        job_url=job_url,
        source_url=source["source_url"],
        source_type=source["source_type"],
        summary=summary[:500],
        language=item.get("language") or "en",
        scraped_at=now_utc().isoformat(),
        scraped_date_bj=today_bj,
        is_new_today=False,
        last_seen_date=today_bj,
        status="active",
    )


def parse_json_api(source: Dict, response_text: str) -> List[Dict]:
    payload = json.loads(response_text)
    options = source.get("options", {})
    data_path = options.get("data_path")
    if data_path:
        for key in str(data_path).split("."):
            if isinstance(payload, dict):
                payload = payload.get(key, [])
    items = payload if isinstance(payload, list) else []
    fmap = options.get("field_map", {})
    job_url_template = options.get("job_url_template", "")

    rows: List[Dict] = []
    for obj in items[: int(options.get("max_items", 200))]:
        job_url = _nested_value(obj, fmap.get("job_url", "url"))
        if not job_url and job_url_template:
            job_url = _render_template(job_url_template, obj)
        rows.append({
            "job_title": _nested_value(obj, fmap.get("job_title", "title")),
            "location": _nested_value(obj, fmap.get("location", "location")),
            "deadline": _nested_value(obj, fmap.get("deadline", "deadline")),
            "posted_date": _nested_value(obj, fmap.get("posted_date", "posted_date")),
            "job_url": job_url,
            "summary": _nested_value(obj, fmap.get("summary", "summary")),
        })
    return rows


def _render_template(template: str, obj: Dict) -> str:
    out = str(template)
    for token in re.findall(r"\{([^{}]+)\}", out):
        out = out.replace("{" + token + "}", _nested_value(obj, token))
    return out


def parse_html_links(source: Dict, html: str) -> List[Dict]:
    options = source.get("options", {})
    keywords = [k.lower() for k in options.get("link_keyword_any", [])]
    url_keywords = [k.lower() for k in options.get("url_keyword_any", [])]
    deny_keywords = [k.lower() for k in options.get("deny_keyword_any", [])]
    deny_url_keywords = [k.lower() for k in options.get("deny_url_keyword_any", [])]
    max_items = int(options.get("max_items", 100))
    min_title_len = int(options.get("min_title_len", 12))
    strict_title = bool(options.get("strict_title_keyword_match", False))
    selectors = options.get("anchor_selectors") or ["a[href]"]
    soup = BeautifulSoup(html, "lxml")

    rows: List[Dict] = []
    seen = set()
    anchors = []
    for selector in selectors:
        anchors.extend(soup.select(selector))
    if not anchors:
        anchors = soup.select("a[href]")

    for a in anchors:
        label = re.sub(r"\s+", " ", a.get_text(" ", strip=True))
        href = a.get("href", "").strip()
        if not label or not href:
            continue
        if href.startswith("#") or href.lower().startswith(("javascript:", "mailto:")):
            continue
        if deny_url_keywords and any(k in href.lower() for k in deny_url_keywords):
            continue
        joined = f"{label} {href}".lower()
        if len(label) < min_title_len:
            continue
        if strict_title and keywords and not any(k in label.lower() for k in keywords):
            continue
        matched_label = (not keywords) or any(k in joined for k in keywords)
        matched_url = (not url_keywords) or any(k in href.lower() for k in url_keywords)
        if not matched_label and not matched_url:
            continue
        if deny_keywords and any(k in joined for k in deny_keywords):
            continue
        url = urljoin(source["source_url"], href)
        key = (label, url)
        if key in seen:
            continue
        seen.add(key)
        rows.append({"job_title": label, "job_url": url, "location": "", "summary": ""})
        if len(rows) >= max_items:
            break
    return rows


def parse_html_structured(source: Dict, html: str) -> List[Dict]:
    options = source.get("options", {})
    keywords = [k.lower() for k in options.get("link_keyword_any", [])]
    deny_keywords = [k.lower() for k in options.get("deny_keyword_any", [])]
    deny_url_keywords = [k.lower() for k in options.get("deny_url_keyword_any", [])]
    container_selectors = options.get("container_selectors") or [
        "article",
        "li",
        "tr",
        "div.job",
        "div.vacancy",
    ]
    max_items = int(options.get("max_items", 120))
    strict_title = bool(options.get("strict_title_keyword_match", False))
    soup = BeautifulSoup(html, "lxml")

    rows: List[Dict] = []
    seen = set()
    for selector in container_selectors:
        for block in soup.select(selector):
            text = re.sub(r"\s+", " ", block.get_text(" ", strip=True))
            if len(text) < 16:
                continue
            low = text.lower()
            if keywords and not any(k in low for k in keywords):
                continue
            if deny_keywords and any(k in low for k in deny_keywords):
                continue

            anchor = block.find("a", href=True)
            if not anchor:
                continue
            title = re.sub(r"\s+", " ", anchor.get_text(" ", strip=True)) or text[:120]
            if strict_title and keywords and not any(k in title.lower() for k in keywords):
                continue
            href = anchor.get("href", "").strip()
            if not href:
                continue
            if deny_url_keywords and any(k in href.lower() for k in deny_url_keywords):
                continue
            url = urljoin(source["source_url"], href)

            loc = _extract_location(text)
            deadline = _extract_deadline(text)
            key = (title, url)
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "job_title": title,
                    "job_url": url,
                    "location": loc,
                    "deadline": deadline,
                    "summary": text[:500],
                }
            )
            if len(rows) >= max_items:
                return rows
    return rows


def _extract_location(text: str) -> str:
    m = re.search(r"(location|duty station|city)\s*[:\-]\s*([A-Za-z ,\-]{2,80})", text, flags=re.I)
    return m.group(2).strip() if m else ""


def _extract_deadline(text: str) -> str:
    m = re.search(r"(deadline|closing date|application deadline)\s*[:\-]\s*([A-Za-z0-9, \-]{4,40})", text, flags=re.I)
    return m.group(2).strip() if m else ""


def parse_rss(source: Dict, xml_text: str) -> List[Dict]:
    options = source.get("options", {})
    keywords = [k.lower() for k in options.get("title_keyword_any", [])]
    deny_keywords = [k.lower() for k in options.get("deny_keyword_any", [])]
    max_items = int(options.get("max_items", 100))
    soup = BeautifulSoup(xml_text, "xml")

    rows: List[Dict] = []
    for item in soup.find_all("item"):
        t = item.find("title")
        title = t.get_text(strip=True) if t else ""
        low_title = title.lower()
        if keywords and not any(k in low_title for k in keywords):
            continue
        if deny_keywords and any(k in low_title for k in deny_keywords):
            continue
        lnk = item.find("link")
        pub = item.find("pubDate")
        desc = item.find("description")
        rows.append({
            "job_title": title,
            "job_url": lnk.get_text(strip=True) if lnk else source["source_url"],
            "posted_date": pub.get_text(strip=True) if pub else "",
            "summary": desc.get_text(" ", strip=True) if desc else "",
            "location": "",
        })
        if len(rows) >= max_items:
            break
    return rows


def parse_workday_api(source: Dict, response_text: str) -> List[Dict]:
    payload = json.loads(response_text)
    options = source.get("options", {})
    max_items = int(options.get("max_items", 120))
    title_keywords = [k.lower() for k in options.get("title_keyword_any", [])]
    deny_keywords = [k.lower() for k in options.get("deny_keyword_any", [])]
    job_host = options.get("job_host") or source.get("source_url", "")

    postings = payload.get("jobPostings", []) if isinstance(payload, dict) else []
    rows: List[Dict] = []
    for post in postings:
        title = str(post.get("title", "")).strip()
        if not title:
            continue
        low = title.lower()
        if title_keywords and not any(k in low for k in title_keywords):
            continue
        if deny_keywords and any(k in low for k in deny_keywords):
            continue

        external_path = str(post.get("externalPath", "")).strip()
        job_url = urljoin(job_host, external_path) if external_path else job_host
        rows.append(
            {
                "job_title": title,
                "job_url": job_url,
                "location": str(post.get("locationsText", "")).strip(),
                "posted_date": str(post.get("postedOn", "")).strip(),
                "summary": " | ".join(post.get("bulletFields", []) or []),
            }
        )
        if len(rows) >= max_items:
            break
    return rows


def parse_oracle_ce_api(source: Dict, response_text: str) -> List[Dict]:
    payload = json.loads(response_text)
    options = source.get("options", {})
    title_keywords = [k.lower() for k in options.get("title_keyword_any", [])]
    deny_keywords = [k.lower() for k in options.get("deny_keyword_any", [])]
    max_items = int(options.get("max_items", 120))
    job_url_template = options.get("job_url_template", "")

    items = payload.get("items", []) if isinstance(payload, dict) else []
    if not items:
        return []
    listing = items[0].get("requisitionList", []) if isinstance(items[0], dict) else []

    rows: List[Dict] = []
    for rec in listing:
        title = str(rec.get("Title", "")).strip()
        if not title:
            continue
        low = title.lower()
        if title_keywords and not any(k in low for k in title_keywords):
            continue
        if deny_keywords and any(k in low for k in deny_keywords):
            continue

        rows.append(
            {
                "job_title": title,
                "location": str(rec.get("PrimaryLocation", "")).strip(),
                "deadline": str(rec.get("PostingEndDate", "")).strip(),
                "posted_date": str(rec.get("PostedDate", "")).strip(),
                "job_url": _render_template(job_url_template, rec) if job_url_template else "",
                "summary": str(rec.get("ShortDescriptionStr", "")).strip(),
            }
        )
        if len(rows) >= max_items:
            break
    return rows


def deduplicate(records: Iterable[JobRecord]) -> List[JobRecord]:
    out: List[JobRecord] = []
    seen = set()
    for rec in records:
        if rec.record_id in seen:
            continue
        seen.add(rec.record_id)
        out.append(rec)
    return out
