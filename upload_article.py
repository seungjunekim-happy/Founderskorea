"""
Markdown 파일을 Founderskorea API로 업로드 + 카테고리 지정 + 발행

Usage:
    python upload_article.py content/articles/some-article.md
    python upload_article.py content/articles/some-article.md --draft     # 발행 안 함
    python upload_article.py content/articles/some-article.md --base http://localhost:8000/api/v1

환경변수:
    ARTICLE_API_KEYS  JSON 형식 {"name": "secret"} (.env에서 자동 로드)
    API_BASE          기본값: https://founderskorea.com/api/v1
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Load .env if exists (no python-dotenv dependency)
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

# Resolve API key
ARTICLE_API_KEYS = os.environ.get("ARTICLE_API_KEYS", "{}")
try:
    keys = json.loads(ARTICLE_API_KEYS)
    if not keys:
        raise ValueError("empty")
    API_KEY = next(iter(keys.values()))
    KEY_NAME = next(iter(keys.keys()))
except Exception:
    print("ERROR: ARTICLE_API_KEYS not configured. Set in .env or environment.")
    sys.exit(1)

# Category label → slug mapping (frontmatter 한글 라벨 → DB slug)
CATEGORY_MAP = {
    "스타트업": "startup",
    "정부지원": "gov-support",
    "투자": "investment",
    "실전노하우": "know-how",
    "네트워킹": "networking",
}


def parse_frontmatter(text: str):
    """Parse simple YAML frontmatter. Returns (meta_dict, body_text)."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 5:].lstrip("\n")

    meta = {}
    for line in fm_text.splitlines():
        line = line.rstrip()
        if not line or ":" not in line or line.startswith("#"):
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            items = [i.strip().strip('"').strip("'") for i in inner.split(",")]
            val = [i for i in items if i]
        meta[key.strip()] = val
    return meta, body


def api_call(method, path, payload=None, base=None):
    url = f"{base}{path}"
    headers = {
        "X-API-Key": API_KEY,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body_bytes = resp.read()
            return json.loads(body_bytes) if body_bytes else {}
    except urllib.error.HTTPError as e:
        try:
            err = e.read().decode("utf-8")
        except Exception:
            err = str(e)
        print(f"ERROR HTTP {e.code} on {method} {path}")
        print(f"       {err}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR network on {method} {path}: {e.reason}")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Upload markdown article to Founderskorea")
    ap.add_argument("file", help="Path to markdown file")
    ap.add_argument("--draft", action="store_true", help="Save as draft (do not publish)")
    ap.add_argument("--base", default=os.environ.get("API_BASE", "https://founderskorea.com/api/v1"),
                    help="API base URL (default: production)")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    title = meta.get("title")
    if not title:
        print("ERROR: No title in frontmatter")
        sys.exit(1)

    # Map fields: subtitle → summary, first tag → tag, category label → slug
    summary = meta.get("subtitle") or meta.get("summary", "")
    tags = meta.get("tags", [])
    tag = tags[0] if isinstance(tags, list) and tags else meta.get("tag", "") or "가이드"
    category_input = meta.get("category", "")
    category_slug = CATEGORY_MAP.get(category_input, category_input)

    print(f"[1/3] 글 생성 — {title[:60]}")
    payload = {
        "title": title,
        "summary": summary,
        "content_md": body,
        "tag": tag,
    }
    if category_slug:
        payload["category_slug"] = category_slug

    res = api_call("POST", "/articles", payload, base=args.base)
    article_id = res["id"]
    slug = res["slug"]
    print(f"      → ID={article_id}, slug={slug}, status=draft")

    if args.draft:
        print(f"[Done] 초안 저장됨. (--draft 모드, 발행 안 함)")
        return

    print(f"[2/3] 발행 — POST /articles/{article_id}/publish")
    pub_res = api_call("POST", f"/articles/{article_id}/publish", payload={}, base=args.base)
    print(f"      → status={pub_res.get('status')}")

    site = args.base.replace("/api/v1", "")
    if category_slug:
        print(f"[3/3] 완료 → {site}/{category_slug}/{slug}")
    else:
        print(f"[3/3] 완료 (카테고리 없음, 사이트에 노출 안 됨 — 카테고리 지정 필요)")


if __name__ == "__main__":
    main()
