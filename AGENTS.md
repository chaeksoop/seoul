# 책숲 (Book Forest) — 프로젝트 컨텍스트

## 개요
서울국제도서전 B109 부스 단일 페이지 웹앱. 컬처룩 + 코쿤북스 협업.

## 저장소
- 로컬: `/Users/dde/Documents/Codex/codex/bookfair`
- 리모트: `git@github.com:dish1218/experiment.git` (main 브랜치)
- 백업 태그: `v1.0-current` (2026-06-18 분석 완료 시점)

## 현재 상태
- 브랜치: `main` (clean, up-to-date with origin/main)
- 구조: 단일 HTML (`index.html` 2131줄) + `css/style.css` (2183줄)
- 데이터: `data/books/{id}.json` (XOR 암호화된 책 본문), 47권 메타데이터는 HTML 내 인라인
- 저장소: localStorage (기대평, 메시지) — 서버/API 없음
- 외부 의존성: Pretendard 폰트, SheetJS (xlsx)

## 핵심 파일
| 파일 | 설명 |
|------|------|
| `index.html` | 전체 앱 (HTML 구조 + JS 로직) |
| `css/style.css` | 모든 스타일 |
| `data/books/1..47.json` | 암호화된 책 본문 (7개만 존재) |
| `scrape_culturlook.py` | 알라딘 크롤러 |
| `book-forest/` | v4 (Firebase, 레거시) |
| `book-forest-v5/` | v5 (레거시, 루트로 교체됨) |

## 주요 기능
1. 책 목록 카드 (확장/축소, 키워드 필터, EVENT 필터)
2. 상단 표지 캐러셀 (자동 스크롤, 클릭 시 팝업)
3. 책 상세 팝업
4. E-Reader (랜덤 챕터, 30초 타이머)
5. 기대평/메시지 (localStorage)
6. 관리자 패널 (로고 5연타 → 기대평/메시지 조회/삭제/엑셀 내보내기)
7. 복사 방지
8. 도서 목록 엑셀 다운로드

## 보안
- 책 본문: XOR(`chaeksoop2024`) + Base64 암호화
- 관리자 암호: `spn3261182` (하드코딩)
- 엑셀 암호: 사용자 입력

## 알려진 이슈 / TODO
- data/books/에 47권 중 7권만 존재 (1,2,3,38,42,46,47)
- localStorage 기반이라 기기별 데이터 분리됨
- 관리자 암호 하드코딩 → 환경변수/설정 파일로 분리 필요
- Firebase 제거됨 (v4에서 v5로 마이그레이션 완료)
- 반응형: 모바일 중심, 태블릿/데스크톱 대응 있음

## 개발 계속하는 방법
```bash
cd /Users/dde/Documents/Codex/codex/bookfair
# 로컬 서버 띄우기 (권장: Live Server or python3 -m http.server)
python3 -m http.server 8000
# 브라우저: http://localhost:8000

# 변경 후 커밋
git add -A && git commit -m "메시지"
git push origin main
```
