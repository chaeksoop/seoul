# 책숲 (Book Forest) — 프로젝트 컨텍스트

## 개요
서울국제도서전 B109 부스 단일 페이지 웹앱. 컬처룩 + 코쿤북스 협업.

## 저장소
- 로컬: `/Users/dde/Documents/Codex/codex/bookfair`
- 리모트: `git@github.com:dish1218/experiment.git` (main 브랜치)
- 백업 태그:
  - `v1.0-current` — 최초 분석 완료 시점
  - `v1.2-final` — 최종 작업 완료 시점 (2026-06-18)

## 현재 상태
- 브랜치: `main` (clean)
- 최종 커밋: `0e23529` (관리자 암호 SHA-256, 크로스 브라우징 패치, git remote SSH)
- 구조: 단일 HTML + CSS, 외부 의존성 최소
- 데이터: `data/books/{id}.json` (XOR 암호화), 47권 메타데이터는 HTML 내 인라인
- 기대평/메시지: localStorage + Firebase Firestore 동기화
- 외부 의존성: Pretendard 폰트, SheetJS (xlsx)

## 복원 방법
```bash
# 1. 클론 또는 기존 저장소로 이동
cd /Users/dde/Documents/Codex/codex/bookfair

# 2. 최신 상태로 복원
git checkout main && git pull origin main

# 3. 특정 백업 지점으로 복원
git checkout v1.2-final

# 4. 로컬 서버 실행
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
| `AGENTS.md` | 프로젝트 컨텍스트 문서 |
| `scrape_culturlook.py` | 알라딘 크롤러 |
| `book-forest/` | v4 (Firebase, 레거시) |
| `book-forest-v5/` | v5 (레거시, 루트로 교체됨) |

## 주요 기능
1. 책 목록 카드 (확장/축소, 키워드 필터, EVENT 필터)
2. 상단 표지 캐러셀 (JS 자동 스크롤 + 드래그, 무한 래핑)
3. 책 상세 팝업
4. E-Reader (랜덤 챕터, 30초 타이머, 다음 읽기)
5. 기대평/메시지 (Firestore 동기화)
6. 관리자 패널 (로고 5연타 → 조회/삭제/엑셀 내보내기)
7. 복사 방지
8. 도서 목록 엑셀 다운로드
9. 부스 메시지 보내기

## 보안
- 책 본문: XOR(`chaeksoop2024`) + Base64 암호화
- 관리자 암호: SHA-256 해시 비교 (crypto.subtle, HTTPS 필요)
- 엑셀 암호: 사용자 입력

## 알려진 이슈 / TODO
- data/books/에 47권 중 7권만 존재 (1,2,3,38,42,46,47)

## 개발 계속하는 방법
```bash
cd /Users/dde/Documents/Codex/codex/bookfair
python3 -m http.server 8000

# 변경 후 커밋 & 푸시
git add -A && git commit -m "설명"
git push origin main
```
