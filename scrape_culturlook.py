#!/usr/bin/env python3
"""
Scrape metadata for 39 컬처룩 books from Aladin.co.kr.
"""
import json
import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from html import unescape

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# For titles that need alternative search queries
CUSTOM_SEARCH = {
    "화이트: 백인 재현의 정치학": "화이트 백인 재현",
    "그래서 함수가 뭐예요?: 수학자가 들려주는 함수 이야기": "그래서 함수가 뭐예요",
    "미백: 피부색의 문화정치": "미백",
    "문화, 이데올로기, 정체성: 스튜어트 홀 선집": "문화 이데올로기 정체성",
}

TITLES = [
    "할리우드 장르",
    "켄 로치: 영화 텔레비전의 정치학",
    "문화, 이데올로기, 정체성: 스튜어트 홀 선집",
    "수학, 영화관에 가다",
    "큐브릭: 그로테스크의 미학",
    "수학은 어떻게 예술이 되었는가",
    "빨강의 문화사: 동굴 벽화에서 디지털까지",
    "루키노 비스콘티: 역사와 개인의 변증법",
    "자연이 만든 가장 완벽한 도형, 나선",
    "자연과 미디어: 고래에서 클라우드까지, 원소 미디어의 철학을 향해",
    "수학 갤러리: 소수에서 미적분까지, 교양으로 읽는 수학 이야기",
    "보드게임하는 수학자",
    "화이트: 백인 재현의 정치학",
    "논문, 쓰다: 대화하는 논문",
    "마음의 말: 정동의 사회적 삶",
    "멋진 우주, 우아한 수학: 기하학으로 본 우주",
    "상징권력과 문화: 부르디외의 이론과 비평",
    "그래서 함수가 뭐예요?: 수학자가 들려주는 함수 이야기",
    "수학이 쉬워지는 미술 놀이: 그리고 만들고 색칠하는 수학",
    "미디어 알고리즘의 욕망: 자동화된 미디어는 우리의 일상을 어떻게 바꾸는가",
    "미백: 피부색의 문화정치",
    "레토릭의 역사와 이론",
    "지중해에서 중세 유럽을 만나다: 십자군 유적지 여행",
    "유럽과 소비에트 변방 기행: 조지아 우크라이나 벨라루스",
    "장애와 텔레비전 문화: 디지털 시대의 재현, 접근, 수용",
    "문화와 사회를 읽는 키워드: 레이먼드 윌리엄스 선집",
    "미디어 내러티브와 스토리텔링",
    "더 단단한 질적 연구를 위한 안내서",
    "미디어와 시대정신의 탄생: 20세기 미디어 사상사",
    "영화, 물질적 유령",
    "의례를 통한 저항: 전후 영국의 청년 하위문화",
    "인종은 피부색이 아니다: 스튜어트 홀의 인종, 종족성, 민족 이론 강의",
    "미장센과 영화 스타일: 고전기 할리우드에서 뉴 미디어 아트까지",
    "글로벌 플랫폼 시대의 K드라마",
    "진실은 여전히 저널리즘의 원칙인가",
    "에코 체임버: 이론적 추적",
    "책임지지 않는 권력: 미디어의 진화, 그 권력 재편과 제도의 사회사",
    "K팝 댄스: 춤, 팬덤, 소셜 미디어",
    "AI 시대에도 미분을 배워야 하나요?",
]


def get_tags(title: str) -> list[str]:
    kw_map = {
        "영화/영상": ["할리우드", "영화", "켄 로치", "큐브릭", "비스콘티", "미장센", "영상", "스크린", "필름"],
        "문화/미디어": ["문화", "미디어", "스튜어트 홀", "정체성", "내러티브", "스토리텔링", "시대정신",
                       "에코 체임버", "레토릭", "키워드", "레이먼드 윌리엄스", "알고리즘"],
        "수학/과학": ["수학", "함수", "미분", "미적분", "소수", "기하학", "나선", "우주", "보드게임"],
        "예술/디자인": ["예술", "디자인", "빨강", "문화사", "미술", "그로테스크"],
        "역사/여행": ["역사", "여행", "지중해", "중세", "십자군", "소비에트", "변방"],
        "사회/정치": ["정치", "이데올로기", "부르디외", "상징권력", "저항", "하위문화", "권력"],
        "인종/젠더": ["화이트", "백인", "미백", "인종", "피부색", "종족성"],
        "철학/사상": ["철학", "사상", "정동"],
        "저널리즘": ["저널리즘", "진실"],
        "장애": ["장애"],
        "K컬처": ["K드라마", "K팝", "케이팝"],
        "논문/연구": ["논문", "질적 연구"],
        "자연/과학": ["자연", "나선", "우주"],
    }
    matched = []
    for tag, kws in kw_map.items():
        if any(kw in title for kw in kws):
            matched.append(tag)
    return matched if matched else ["기타"]


def clean(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch(url: str, params: dict | None = None, max_retries: int = 3) -> str | None:
    for attempt in range(max_retries):
        try:
            resp = SESSION.get(url, params=params, timeout=25)
            resp.encoding = "utf-8"
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            print(f"    HTTP error: {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return None


def parse_search_result(box: BeautifulSoup) -> dict | None:
    links = box.find_all("a", href=True)
    item_id = None
    title_text = ""

    for a in links:
        href = a["href"]
        txt = a.get_text(strip=True)
        m = re.search(r"wproduct\.aspx\?ItemId=(\d+)", href)
        if m and txt and len(txt) > 1 and "#" not in href:
            iid = int(m.group(1))
            skip_words = {"크게보기", "보러 가기", "장바구니", "바로구매", "보관함", "마이리스트"}
            if txt not in skip_words:
                if not item_id or len(txt) > len(title_text):
                    item_id = iid
                    title_text = txt

    full_joined = box.get_text(" ", strip=True)

    # Extract the author section: between last "ㅣ" (series) and first "|" (publisher divider)
    # Also handle cases without series info
    author_section = full_joined
    parts_by_pipe = full_joined.split("|")
    if len(parts_by_pipe) >= 2:
        # Before the first "|" is author info (sometimes preceded by series)
        author_section = parts_by_pipe[0]
    # Remove anything before the last "ㅣ" (series name)
    last_series_marker = author_section.rfind("ㅣ")
    if last_series_marker >= 0:
        author_section = author_section[last_series_marker + 1:].strip()

    author_parts = re.findall(
        r'([가-힣A-Za-z\s.]+?)\s*\((지은이|옮긴이|엮은이|편역|그림|글|사진|감수)\)',
        author_section,
    )
    author_text = ""
    if author_parts:
        author_text = ", ".join(
            f"{name.strip()} ({role})" for name, role in author_parts
        )

    publisher_text = ""
    pub_match = re.search(r'[|]\s*(컬처룩|코쿤북스[^\d]*)\s*[|]', full_joined)
    if pub_match:
        publisher_text = pub_match.group(1).strip()
    elif "컬처룩" in full_joined:
        publisher_text = "컬처룩"

    if not item_id:
        return None

    return {
        "item_id": item_id,
        "title": title_text,
        "author": author_text,
        "publisher": publisher_text,
        "full_text": full_joined,
    }


def search_aladin(query: str) -> list[dict]:
    html = fetch(
        "https://www.aladin.co.kr/search/wsearchresult.aspx",
        {"SearchTarget": "All", "SearchWord": query},
    )
    if not html:
        return []
    soup = BeautifulSoup(html, "lxml")
    candidates = []
    for box in soup.select("div.ss_book_box"):
        parsed = parse_search_result(box)
        if parsed:
            candidates.append(parsed)
    return candidates


def generate_queries(title: str) -> list[str]:
    """Generate search queries in order of specificity."""
    queries = []

    # 1. Custom override
    if title in CUSTOM_SEARCH:
        queries.append(CUSTOM_SEARCH[title])

    # 2. Full title stripped of special chars
    simplified = re.sub(r"[,:;]+", " ", title)
    simplified = re.sub(r"\s+", " ", simplified).strip()
    if simplified != title:
        queries.append(simplified)

    # 3. Full title
    queries.append(title)

    # 4. Before first colon
    if ":" in title:
        before_colon = title.split(":")[0].strip()
        queries.append(before_colon)

    # 5. Before first comma (if different)
    if "," in title.split(":")[0] if ":" in title else "," in title:
        before_comma = (title.split(":")[0] if ":" in title else title).split(",")[0].strip()
        if before_comma and before_comma not in queries:
            queries.append(before_comma)

    return queries


def fetch_product(item_id: int) -> dict | None:
    html = fetch(
        "https://www.aladin.co.kr/shop/wproduct.aspx",
        {"ItemId": item_id},
    )
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")
    og_image = ""
    og_description = ""
    author = ""

    for meta in soup.find_all("meta"):
        prop = meta.get("property", "") or meta.get("name", "") or meta.get("itemprop", "")
        content = meta.get("content", "")
        if prop in ("og:image", "image") and not og_image:
            if content.startswith("http"):
                og_image = content
        elif prop in ("og:description", "description", "twitter:description"):
            if not og_description and len(content) > 10:
                og_description = content
        elif prop in ("author", "og:author") and not author:
            if content.strip():
                author = content.strip()

    if not og_description or len(og_description) < 30:
        for sel in [".Egov_summary", ".conts_view", ".summary"]:
            el = soup.select_one(sel)
            if el:
                txt = clean(el.get_text(" ", strip=True))
                if len(txt) > 20:
                    og_description = txt[:500]
                    break

    return {"og_image": og_image, "og_description": og_description, "author": author}


def process_book(title: str, index: int, total: int) -> dict:
    print(f"[{index+1}/{total}] {title}", file=sys.stderr)

    result = {
        "title": title,
        "author": "",
        "itemId": None,
        "coverUrl": "",
        "description": "",
        "tags": get_tags(title),
        "found": False,
    }

    queries = generate_queries(title)
    all_candidates = []

    for q in queries:
        candidates = search_aladin(q)
        if candidates:
            # Filter to keep only those from 컬처룩 (or unknown publisher)
            for c in candidates:
                c["_query"] = q
            all_candidates.extend(candidates)
            # If we found 컬처룩 books, prefer those
            cul_candidates = [c for c in candidates if "컬처룩" in c.get("publisher", "")]
            if cul_candidates:
                break

    if not all_candidates:
        print(f"  ! No search results with any query", file=sys.stderr)
        return result

    # Score: prefer 컬처룩 publisher + title match
    def score(c):
        s = 0
        pub = c.get("publisher", "")
        if "컬처룩" in pub:
            s += 20
        c_title = c.get("title", "")
        title_core = title.split(":")[0].strip().rstrip(",")
        if title_core in c_title or c_title in title_core:
            s += 10
        # Penalize if clearly wrong
        if c_title and title_core and len(title_core) > 2:
            # Check if at least some Korean words overlap
            c_kw = set(re.findall(r"[가-힣]+", c_title))
            t_kw = set(re.findall(r"[가-힣]+", title_core))
            if c_kw and t_kw and not c_kw & t_kw:
                s -= 20
        return s

    all_candidates.sort(key=score, reverse=True)
    best = all_candidates[0]

    # Try the best candidate
    item_id = best["item_id"]
    author = best.get("author", "")
    best_title = best.get("title", "")
    best_pub = best.get("publisher", "")
    print(f"  ~ Best: ItemId={item_id} pub='{best_pub}' title='{best_title}'", file=sys.stderr)

    prod = fetch_product(item_id)
    if not prod:
        print(f"  ! Could not fetch product page", file=sys.stderr)
        return result

    result["itemId"] = item_id
    result["coverUrl"] = prod.get("og_image", "")
    result["description"] = prod.get("og_description", "")[:300] if prod.get("og_description") else ""
    # Prefer product-page author (cleaner), fall back to search-result author
    raw_author = prod.get("author", "") or author
    raw_author = raw_author.strip().lstrip(",").strip().lstrip(",").strip()
    result["author"] = raw_author
    result["found"] = True
    display_author = result["author"][:30] if result["author"] else "?"
    print(f"  ✓ author={display_author} cover={'yes' if result['coverUrl'] else 'no'}", file=sys.stderr)

    time.sleep(0.5)
    return result


def main():
    out_path = "/Users/dde/Documents/bookfair/책숲/data/culturlook_books.json"
    total = len(TITLES)
    results = []

    for i, title in enumerate(TITLES):
        r = process_book(title, i, total)
        results.append(r)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    found = sum(1 for r in results if r["found"])
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Done. {found}/{total} books found.", file=sys.stderr)


if __name__ == "__main__":
    main()
