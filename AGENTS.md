# 책숲 (Book Forest) — 프로젝트 컨텍스트

## 개요
서울국제도서전 B109 부스 단일 페이지 웹앱. 컬처룩 + 코쿤북스 협업.
- 행사 기간: 2026-06-24 ~ 2026-06-29
- 부스: B109

## 저장소
- 로컬: `/Users/dde/Documents/Codex/codex/bookfair`
- 리모트: `https://github.com/chaeksoop/seoul.git` (master 브랜치 — Pages 기준)
- Pages: `https://chaeksoop.github.io/seoul/`
- 푸시: `git push origin master` (※ master 브랜치만 Pages에 반영됨)
- 태그: `git push origin master --tags`
- 백업 태그:
  - `v1.0-current` — 최초 분석 완료 시점
  - `v1.2-final` — UI/기능 마무리 (2026-06-18)
  - `v1.3-cross-browser` — 크로스 브라우징 및 보안 개선 (2026-06-19)
  - `v1.4-supplement` — ISBN 부가기호 5자리 적용 (2026-06-19)
  - `v1.5-review-carousel` — 리뷰 캐러셀 + 모바일 간격 조정 (2026-06-19)
  - `v1.6-reading-samples` — 3종 이벤트 도서 읽기 샘플 추가 (2026-06-20)
  - `v1.7-security-fixes` — 보안 수정 (프로토타입 오염, XSS, 에러 처리) (2026-06-21)
  - `v1.8-reading-sample-38` — 영화, 물질적 유령 읽기 자료 추가 (2026-06-21)

## 현재 상태
- 브랜치: `master` (clean, working tree)
- 최종 커밋: `972e1c5` (AGENTS.md 업데이트)
- 페이지 제목: "책숲 - 책의 숲에서 잠시 멈춤."
- 관리자 접근: 로고 5회 클릭 → 암호 입력 (`lkjh11`)
- 관리자 암호 SHA-256: `f7a4368b1d02b33a2c56979c09392aa47a521518505e0918959a3f147bf68242`
- 구조: 단일 HTML + CSS, 외부 의존성 최소
- 데이터: `data/books/{id}.json` (XOR 암호화), 47권 메타데이터는 HTML 내 인라인
- 기대평/메시지: localStorage + Firebase Firestore 동기화
- 외부 의존성: Pretendard 폰트, SheetJS (xlsx), Firebase Firestore
- Firebase 프로젝트: `chaeksoop`
- 리뷰 캐러셀: Firestore 리뷰를 홈 상단에 5초 간격 회전 (커버 캐러셀 위)
- 모바일 간격 조정: header, brand-bar, carousel, filter, event-notice, footer 간격 압축 (~100px)
- 읽기 샘플: 4종 이벤트 도서
  - id:38 영화, 물질적 유령 (10장)
  - id:42 AI 시대에도 미분을 배워야 하나요? (7장)
  - id:46 책임지지 않는 권력 (10장)
  - id:47 K팝 댄스 (7장)

## 보안 현황
### 적용 완료
- XSS 방어: `escapeHtml()`로 모든 사용자 입력 렌더링
- 프로토타입 오염: `{...d.data()}` → 명시적 필드 추출 (reviews, messages)
- 인라인 onclick 제거 → `addEventListener`
- catch 블록: 8개 전부 `console.error` 로깅
- Reader null 체크: `chapters`, `paragraphs` 안전 접근
- Mailto: `encodeURIComponent` 적용
- 중복 리뷰 방지: sessionStorage 기반
- 이중 submit 제거: attachReviewSubmit 본문 제거 (delegation만 사용)
- 복사 방지 제거: `user-select:none` + 이벤트 차단 모두 제거 (접근성)

### 미해결 (Firebase Console 필요)
- **CRITICAL**: Firestore 보안 규칙 미설정 (누구나 읽기/쓰기/삭제 가능)
- **HIGH**: 관리자 인증이 클라이언트 측 암호뿐임
- **MEDIUM**: 이메일 평문 저장 (Firestore에 raw email)

### 권장 Firestore 규칙
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /reviews {
      allow read: if true;
      allow create: if request.resource.data.keys().hasAll(['id','bookId','text','createdAt'])
                     && request.resource.data.text is string
                     && request.resource.data.text.size() < 500;
      allow delete, update: if false;
    }
    match /messages {
      allow read: if true;
      allow create: if request.resource.data.keys().hasAll(['id','text'])
                     && request.resource.data.text is string;
      allow delete, update: if false;
    }
    match /{document=**} { allow read, write: if false; }
  }
}
```

## 복원 방법
```bash
cd /Users/dde/Documents/Codex/codex/bookfair
git checkout master && git pull origin master
python3 -m http.server 8000
# 브라우저: http://localhost:8000
```

## 핵심 파일
| 파일 | 설명 |
|------|------|
| `index.html` | 전체 앱 (HTML 구조 + JS 로직, 2486줄) |
| `css/style.css` | 모든 스타일 (2306줄) |
| `data/books/{id}.json` | XOR 암호화된 책 본문 (7개: 1,2,3,38,42,46,47) |
| `images/` | 책 표지, 로고 이미지 |
| `scrape_culturlook.py` | 알라딘 크롤러 |
| `AGENTS.md` | 프로젝트 컨텍스트 (이 파일) |

## 주요 의사결정
- CSP `<meta>` 태그 제외: Firebase connect-src 도메인을 전부 명시할 수 없어 기능 차단 위험
- IIFE 래핑 제외: 전역 함수 참조 깨짐 방지
- SHA-256 폴백 구현: `crypto.subtle` 없는 HTTP 환경 대응 (JS 순수 구현)
- XOR 암호화: 콘텐츠 보호보다는 우발적 접근 방지 목적 (보안 아님)

## 알려진 이슈 / TODO
- `data/books/`에 47권 중 7권만 존재 (1,2,3,38,42,46,47)
- Firestore 보안 규칙 Firebase Console에서 수동 설정 필요
- 관리자 삭제 필요 시 Firebase Console에서 직접 문서 삭제
