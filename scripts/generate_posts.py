"""
엑셀 파일을 Astro 콘텐츠 컬렉션용 Markdown 파일로 변환합니다.

설치:
  pip install pandas openpyxl

사용:
  python scripts/generate_posts.py input/posts.xlsx

엑셀 권장 열:
  id, title, slug, description, pubDate, category, tags, content, status

- status가 'published' 또는 '발행'인 행만 생성합니다.
- tags는 쉼표로 구분합니다.
- slug는 영문 소문자/숫자/하이픈 사용을 권장합니다.
- 생성 전 기존 파일을 덮어쓰지 않도록 기본 설정되어 있습니다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from datetime import date, datetime

try:
    import pandas as pd
except ImportError:
    raise SystemExit("필요한 패키지가 없습니다. 먼저 실행하세요: pip install pandas openpyxl")

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "src" / "content" / "posts"
ALLOWED_CATEGORIES = {"건강", "생활 정보", "뉴스", "기타"}

def clean(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()

def yaml_quote(value: str) -> str:
    # JSON 문자열은 YAML의 큰따옴표 문자열로도 유효합니다.
    import json
    return json.dumps(value, ensure_ascii=False)

def safe_slug(value: str) -> str:
    slug = value.strip().lower()
    slug = re.sub(r"[^a-z0-9가-힣-]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    if not slug:
        raise ValueError("slug가 비어 있습니다. 엑셀에 고유 slug를 입력하세요.")
    return slug

def parse_date(value) -> str:
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")
    text = clean(value)
    if not text:
        return date.today().strftime("%Y-%m-%d")
    parsed = pd.to_datetime(text, errors="raise")
    return parsed.strftime("%Y-%m-%d")

def make_markdown(row: dict) -> tuple[str, str]:
    title = clean(row.get("title"))
    slug = safe_slug(clean(row.get("slug")) or clean(row.get("id")))
    description = clean(row.get("description"))
    content = clean(row.get("content"))
    category = clean(row.get("category")) or "기타"
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"지원하지 않는 category: {category}")
    if not title or not description or not content:
        raise ValueError("title, description, content는 필수 항목입니다.")
    pub_date = parse_date(row.get("pubDate"))
    tags_raw = clean(row.get("tags"))
    tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]
    tags_yaml = "\n".join(f"  - {yaml_quote(tag)}" for tag in tags) or "  []"
    frontmatter = (
        "---\n"
        f"title: {yaml_quote(title)}\n"
        f"description: {yaml_quote(description)}\n"
        f"pubDate: {pub_date}\n"
        f"category: {yaml_quote(category)}\n"
        "tags:\n"
        f"{tags_yaml}\n"
        "draft: false\n"
        "---\n\n"
    )
    return slug, frontmatter + content + "\n"

def main() -> int:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "input" / "posts.xlsx"
    if not input_path.exists():
        print(f"엑셀 파일을 찾을 수 없습니다: {input_path}")
        print("엑셀 파일을 input/posts.xlsx에 넣거나 경로를 인수로 지정하세요.")
        return 1

    frame = pd.read_excel(input_path, dtype=object)
    required = {"title", "description", "pubDate", "category", "content"}
    missing = required - set(frame.columns)
    if missing:
        print("엑셀에 필수 열이 없습니다:", ", ".join(sorted(missing)))
        return 1

    if "status" in frame.columns:
        frame = frame[frame["status"].astype(str).str.strip().str.lower().isin({"published", "발행"})]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    existing_slugs = set()
    generated = 0
    errors = 0

    for idx, series in frame.iterrows():
        row = series.to_dict()
        try:
            slug, markdown = make_markdown(row)
            if slug in existing_slugs:
                raise ValueError(f"이번 실행에서 slug 중복: {slug}")
            existing_slugs.add(slug)
            target = OUTPUT_DIR / f"{slug}.md"
            if target.exists():
                raise FileExistsError(f"기존 파일이 있어 덮어쓰지 않습니다: {target}")
            target.write_text(markdown, encoding="utf-8")
            generated += 1
            print(f"[생성 완료] {target.relative_to(ROOT)}")
        except Exception as exc:
            errors += 1
            print(f"[행 {idx + 2} 오류] {exc}")

    print(f"\n완료: {generated}개 생성, {errors}개 오류")
    print("생성 파일을 확인한 뒤 프로젝트 폴더를 GitHub에 업로드하세요.")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
