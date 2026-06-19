# 책숲 (Book Forest) — 프로젝트 컨텍스트

## 개요
서울국제도서전 B109 부스 단일 페이지 웹앱. 컬처룩 + 코쿤북스 협업.

## 저장소
- 로컬: `/Users/dde/Documents/Codex/codex/bookfair`
- 리모트: `git@github.com:dish1218/experiment.git` (main 브랜치)
- 백업 태그:
  - `v1.0-current` — 최초 분석 완료 시점
  - `v1.2-final` — UI/기능 마무리 (2026-06-18)
  - `v1.3-cross-browser` — 크로스 브라우징 및 보안 개선 (2026-06-19)
  - `v1.4-supplement` — ISBN 부가기호 5자리 적용 (2026-06-19)

## 현재 상태
- 브랜치: `main` (clean, working tree)
- 최종 커밋: `2d76e95` (ISBN 부가기호 5자리로 교체)
- 구조: 단일 HTML + CSS, 외부 의존성 최소
- 데이터: `data/books/{id}.json` (XOR 암호화), 47권 메타데이터는 HTML 내 인라인
- 기대평/메시지: localStorage + Firebase Firestore 동기화
- 외부 의존성: Pretendard 폰트, SheetJS (xlsx)
- 리뷰 캐러셀: Firestore 리뷰를 홈 상단에 5초 간격 회전 (커버 캐러셀 위)
- 모바일 간격 조정: header, brand-bar, carousel, filter, event-notice, footer 간격 압축 완료

## 복원 방법
```bash
cd /Users/dde/Documents/Codex/codex/bookfair
git checkout main && git pull origin main
python3 -m http.server 8000
# 브라우저: http://localhost:8000
```

## 핵심 파일
| 파일 | 설명 |
|------|------|
| `index.html` | 전체 앱 (HTML 구조 + JS 로직) |
| `css/style.css` | 모든 스타일 |
| `data/books/1..47.json` | 암호화된 책 본문 (7개만 존재) |
| `images/` | 책 표지, 로고 이미지 |
| `scrape_culturlook.py` | 알라딘 크롤러 |

## 알려진 이슈 / TODO
- data/books/에 47권 중 7권만 존재 (1,2,3,38,42,46,47)
