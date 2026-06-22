# 책숲 (Book Forest) — 프로젝트 컨텍스트

## 개요
서울국제도서전 B109 부스 단일 페이지 웹앱. 컬처룩 + 코쿤북스 협업.
- 행사 기간: 2026-06-24 ~ 2026-06-29
- 부스: B109
- 페이지 제목: "책숲 - 책의 숲에서 잠시 멈춤."
- 사이트: https://chaeksoop.github.io/seoul/

## 저장소
- 로컬: `/Users/dde/Documents/Codex/codex/bookfair`
- 리모트: `https://github.com/chaeksoop/seoul.git` (master 브랜치 — Pages 기준)
- Pages: `https://chaeksoop.github.io/seoul/`
- 푸시: `git push origin master` (※ master 브랜치만 Pages에 반영됨)
- 태그: `git push origin master --tags`
- 로컬 테스트: `python3 -m http.server 8000` → `http://localhost:8000`

## 브랜치
- `master` (유일; Pages 배포 기준)

## 태그 히스토리
| 태그 | 설명 |
|------|------|
| `v1.0-current` | 최초 분석 완료 시점 |
| `v1.2-final` | UI/기능 마무리 (2026-06-18) |
| `v1.3-cross-browser` | 크로스 브라우징 및 보안 개선 (2026-06-19) |
| `v1.4-supplement` | ISBN 부가기호 5자리 적용 (2026-06-19) |
| `v1.5-review-carousel` | 리뷰 캐러셀 + 모바일 간격 조정 (2026-06-19) |
| `v1.6-reading-samples` | 3종 이벤트 도서 읽기 샘플 추가 (2026-06-20) |
| `v1.7-security-fixes` | 보안 수정 (프로토타입 오염, XSS, 에러 처리) (2026-06-21) |
| `v1.8-reading-sample-38` | 영화, 물질적 유령 읽기 자료 추가 (2026-06-21) |
| `v1.9-final` | review CSS 정리, 리스너 누수, z-index, interval 정리 |
| `v1.10-locked` | admin panel 제거, Firestore rules 잠금, auto-approve |
| `v1.11-final` | 복사 방지 추가 (user-select + 이벤트 차단) |
| `v1.12-final` | 북카드 리뷰 잘림 fix |
| `v1.13-final` | 문구 통일/성공 팝업 분리 |
| `v1.14-backup` | 뒤로가기 popstate 처리 백업 |
| `v1.15-backup` | 북 팝업 버튼 auto-scroll 백업 |

---

## 사이트 구조 (HTML)

### 정적 섹션 (index.html)
```
<head>
  ├── charset UTF-8, viewport, title, OG meta
  ├── Pretendard 폰트 (preconnect + stylesheet)
  ├── css/style.css
  └── SheetJS (xlsx) + Firebase compat SDK (v10.14.1)
<body> ─── border-top: 4px solid #8BAA8A
<div class="container"> ─── max-width: 640px → 720px(tablet)
  ├── <header> ─── 배경 트리패턴 / 로고 / 태그라인
  │   ├── <h1 id="logo"> 🌲 책<span>숲</span> 🌿
  │   └── <p id="tagline"> 책의 숲에서 잠시 멈춤.
  ├── <div class="brand-bar"> ─── 브랜드 정보
  │   ├── <span class="booth-info"> 서울국제도서전 · B109
  │   └── <span class="brand-publishers"> 컬처룩 · 코쿤북스
  ├── <div class="review-carousel" id="reviewCarousel"> ─── 리뷰 캐러셀
  ├── <div class="cover-carousel" id="coverCarousel"> ─── 표지 캐러셀
  ├── <button class="filter-trigger" id="filterTrigger"> ─── 키워드 필터
  ├── <div class="event-notice" id="eventFilter"> ─── 이벤트 박스
  ├── <div class="book-list" id="bookList"> ─── 책 카드 그리드
  └── <footer class="footer">
      ├── <button id="floatingDownloadBtn"> 📋 전체 도서목록 다운로드
      ├── <button id="floatingMsgBtn"> 💬 부스에 메시지 보내기
      └── <p> 책숲 · 서울국제도서전 B109 / © 2026 컬처룩 · 코쿤북스
```

### 팝업/모달/오버레이 (9개)
| ID | 타입 | z-index | 내용 |
|----|------|---------|------|
| `bookPopupOverlay` | 팝업 | 900 | 책 상세 (표지, 메타, 설명, 버튼) |
| `chipsModal` | 모달 | 171 | 키워드 필터 칩 선택 |
| `readerOverlay` | 전체화면 | 2000 | E-Reader (챕터 읽기) |
| `completionPopup` | 팝업 | 3000 | 읽기 완료 안내 |
| `reviewSuccessPopup` | 팝업 | 3100 | 리뷰 제출 완료 (+confetti) |
| `reviewListPopup` | 팝업 | 3101 | 모든 기대평 목록 |
| `floatingStopBtn` | 플로팅 | 1500 | ✍️ 기대평 쓰기 (읽기 중 표시) |
| `stopDrawer` | 드로어 | 1800 | 리뷰 작성 폼 (바텀시트) |
| `msgModal` | 모달 | 161 | 부스 메시지 보내기 |

### E-Reader 구조
- 고정 전체화면 오버레이, 종이톤 배경(#F5F0E8)
- 헤더: sticky, 뒤로가기 + 제목/저자 + 타이머(00:00 / 00:30) + 진행바
- 본문: `max-width: 640px`, 단락 + 이미지 렌더링
- 하단(next-chapter): fixed, gradient fade-up, `다음 읽기` / `기대평 쓰고 굿즈 받기` 버튼
- 30초 타이머 완료 시 리뷰 버튼 활성화 + 완료 팝업

---

## 47권 도서 컬렉션

### 출판사별 분포
- **컬처룩**: 40권 (id 9~47; 단행본/영화/미디어/수학/문화연구)
- **코쿤북스**: 7권 (id 1~8, 단 4번 `포에버 도그` 제외 6권)

### 이벤트 도서 (7권)
| ID | 제목 | 저자 | 출판사 |
|----|------|------|--------|
| 1 | 창조적 행위: 존재의 방식 | 릭 루빈 | 코쿤북스 |
| 2 | 뒷마당 탐조 클럽 | 에이미 탄 | 코쿤북스 |
| 3 | 새와 나무와 돌멩이의 지적 세계 | 제임스 브라이들 | 코쿤북스 |
| 38 | 영화, 물질적 유령 | 질베르토 페레스 | 컬처룩 |
| 42 | AI 시대에도 미분을 배워야 하나요? | 이한진 | 컬처룩 |
| 46 | 책임지지 않는 권력 | 제임스 커런 | 컬처룩 |
| 47 | K팝 댄스: 춤, 팬덤, 소셜 미디어 | 오주연 | 컬처룩 |

### 메타데이터 필드 (window.books 배열)
`id`, `title`, `titleEn`, `subtitle`, `author`, `authorEn`, `tags`, `description`, `excerpt`, `publisher`, `color`, `image`, `isbn`, `kdc`, `price`, `pages`, `event`(boolean)

### KDC 분류 체계
- 앞 2자리 + 3자리 부가기호로 카테고리 매핑 (KDC_CATEGORIES 60+항목)
- 첫째 자리 대분류 (KDC_MAJOR): 0 총류, 1/8 인문학, 2 종교, 3 사회과학, 4/5 과학, 6 예술, 7 언어, 9 역사

---

## 기능 상세

### 1. 커버 캐러셀 (cover-carousel)
- 상단 가로 스크롤, 47권 표지를 CSS 애니메이션으로 자동 롤링 (60s linear infinite)
- 드래그/터치 스크롤 지원 (mousedown/mousemove/mouseup + touchstart/touchmove/touchend)
- 클릭 시 `openBookPopup` 호출
- `buildCarousel(eventOnly?)`: eventOnly=true 시 이벤트 도서만 표시
- 자동 스크롤: JS requestAnimationFrame 0.4px/frame
- 드래그 후 4초 idle 시 재개

### 2. 리뷰 캐러셀 (review-carousel)
- Firestore `reviews` 컬렉션에서 불러온 승인된 리뷰를 5초 간격 회전
- `has-reviews` 클래스로 높이 전환 (0→48px)
- 리뷰 슬라이드 fade-in/out (0.6s transition)
- 클릭 시 `openReviewList()` → 모든 기대평 리스트 팝업
- 빈 상태: 캐러셀 숨김 (height:0)

### 3. 키워드 필터 (chips-modal)
- 23개 키워드 칩: `새, 자연, 식물, 에세이, 과학, 생태, 힐링, 영감, 그림책, 반려동물, 건강, 심리, 문학, 영화, 미디어, 수학, 예술, 역사, 사회, 인종, K문화, 창작, 창조성`
- 칩 클릭 시 활성화/비활성화 (다중 선택 가능)
- 활성 칩에 해당하는 책만 필터링 (이벤트 도서 우선 정렬)
- 트리거 버튼에 활성 태그 개수 badge 표시
- 필터 초기화 기능 (✕)
- 일치하는 책 없음: `해당 키워드의 책이 없습니다. 다른 키워드를 선택해보세요.`

### 4. 이벤트 박스 (event-notice)
- `🎁 EVENT` 헤더 + 설명 + `클릭해서 펼치기` hint
- 펼치면 이벤트 도서 7권 북카드 랜덤 정렬 표시
- CSS: `max-width: 480px`에서 padding 확장, active 시 gradient 진하게
- 뒤로가기(popstate) 시 자동 접기 + renderBooks/buildCarousel 복원

### 5. 북카드 (book-card)
- 표지 + 태그 + 제목 + 저자 + excerpt
- 이벤트 도서: 오렌지 `이벤트` 뱃지 + `이벤트 참여하기` 버튼
- 클릭 시 펼쳐짐 애니메이션 (height: 0 → auto, 0.4s)
- 펼쳐진 영역: 설명, 인용구, 출판사, 최대 3개 랜덤 리뷰, 읽기 버튼
- 리뷰가 펼침 영역 밖으로 튀어나오지 않도록 `overflow: visible`(expanded 시) 처리
- 모바일: flex column 단일 열; 태블릿(768px↑): 2열 grid

### 6. 북 팝업 (book-popup)
- 표지(좌) + 정보(우) 레이아웃 (400px, 90vh)
- 정보 영역: 제목/영문제목/부제/저자/메타(KDC·가격·쪽수·ISBN) → 설명 → 인용구 → 출판사 → 버튼
- 이벤트 도서: `⏱️ 이벤트 참여하기` → E-Reader 오픈
- 일반 도서: `✍️ 리뷰 작성하기` → 리뷰 폼 드로어 오픈
- 오픈 시 `setTimeout(400ms)` 후 버튼 위치로 `scrollIntoView({block:'center', behavior:'smooth'})`
- 오버레이 클릭/✕ 버튼으로 닫기

### 7. E-Reader (reader-overlay)
- `openReader(bookId)`: data/books/{id}.json XOR 복호화 후 랜덤 미읽 챕터 로드
- 타이머: 1초 간격, 30초 카운트 (진행바 애니메이션)
- 30초 완료 시 `readerCompleted=true`, 리뷰 버튼 활성화, 완료 팝업 표시
- `다음 읽기`로 다른 챕터 로드 (중복 없이, 모두 읽으면 "다 읽었습니다" 안내)
- 이미지 렌더링 (백슬래시로 감싸진 URL → img 태그 변환)
- 하단 리뷰 버튼은 스크롤 위치와 completed 상태에 따라 show/hide
- 플로팅 `✍️ 기대평 쓰기` 버튼 (reader 오픈 시 표시, 종료 시 숨김)
- 완료 팝업: `🎉 읽기 완료!` + `📖 계속 읽기` / `🎁 기대평 쓰고 굿즈 받기`

### 8. 리뷰 시스템 (reviews)
- **Firestore 컬렉션**: `reviews`
- **필드**: `id`(auto), `bookId`(number), `name`(string), `text`(string), `email`(string), `createdAt`(string), `approved`(boolean, auto=true), `event`(boolean)
- **제출**: stopDrawer 바텀시트에서 폼 제출
  - 이벤트 도서: `기대평 남기고 굿즈 받기` / placeholder `인상적인 구절이나 기대평을 남겨주세요`
  - 일반 도서: `리뷰 남기기` / placeholder `인상적인 구절이나 리뷰를 남겨주세요`
  - 추가 필드: 읽은 시간 표시, 이름, 이메일(선택), 개인정보 동의(이벤트만)
- **유효성 검사**: 이름/내용 필수, profanity filter(21개 금칙어), Firestore 중복 쿼리
- **성공 팝업**:
  - 이벤트: `이벤트 참여 감사합니다!` + `부스 스태프에게 화면을 보여주고 굿즈를 받아가세요. :)` + confetti
  - 일반: `소중한 리뷰 감사합니다!` + `이벤트에도 참여해보세요` (confetti 없음)
- **리스트 팝업**: 모든 승인된 리뷰를 랜덤 순서로 표시
- **북카드 리뷰**: 펼쳐진 카드에 최대 3개 랜덤 리뷰 표시

### 9. 메시지 모달 (messages)
- **Firestore 컬렉션**: `messages`
- **필드**: `id`(auto), `name`(string), `text`(string), `contact`(string), `createdAt`(string)
- 우측 하단 `💬 부스에 메시지 보내기` 버튼으로 오픈
- 입력: 이름(선택), 메시지(필수, 500자 제한), 이메일(선택)
- 성공 시: `✅ 메시지가 전송되었습니다. 소중한 의견 감사합니다.`

### 10. 엑셀 다운로드 (SheetJS)
- `📋 전체 도서목록 다운로드` 버튼
- 47권 모든 메타데이터를 XLSX로 추출
- 컬럼: ID, 제목, 제목(영문), 부제, 저자, 저자(영문), 출판사, ISBN, KDC, 분야, 정가, 쪽수, 태그, 설명, 책 속 한 줄, 이벤트
- 파일명: `책숲_도서목록.xlsx`

### 11. 키워드 칩 모달 (chips-modal)
- 23개 키워드를 랜덤 순서로 렌더링
- 다중 선택 가능, 선택 시 해당 태그 보유 도서만 필터링
- 모달 backdrop 클릭 또는 ✕ 버튼으로 닫기

### 12. 복사 방지
- `user-select: none` (body CSS)
- 이벤트 차단: `copy`, `contextmenu`(우클릭), `selectstart` → `preventDefault()`
- `selectionchange`: input/textarea 외 선택 즉시 제거
- `keydown`: Ctrl/Cmd+C 차단

### 13. 뒤로가기 처리 (popstate)
- 모든 팝업/모달/오버레이 오픈 시 `history.pushState({popup:true}, '')`
- `window.addEventListener('popstate', closeAllOverlays)`
- `closeAllOverlays()`가 닫는 대상:
  - 모든 `.open` 클래스 요소 (북팝업, 리뷰리스트, 리더, 컴플리션, 리뷰성공, 칩모달, 메시지모달, 스탑드로어)
  - `#eventFilter.active` (이벤트 박스 접기 + renderBooks/buildCarousel 복원)
  - reader 타이머, currentReaderBookId, floatingStopBtn, confetti 정리

### 14. Confetti
- canvas 기반, 120개 조각, 7가지 색상 (#A8C9A5, #D4A853, #E8A87C, #85CDCA, #F4A7A7, #B8A8D8, #F7DC6F)
- 중력 + 바람 효과, ~6초 지속, requestAnimationFrame
- 이벤트 도서 성공 팝업에서만 표시

### 15. Profanity 필터 (BAD_WORDS)
- 21개 키워드: `시발, 씨발, 시팔, 씹, 존나, 좆, 병신, 새끼, 느금마, 개새끼, 미친, 니미럴, 호로, 십새, 십팔, ㄱㅅㄲ, ㅅㅂ, fuck, shit, asshole, bitch, bastard, dick, porn, sex, free money, click here, buy now, subscribe, http://, https://`
- 대소문자 구분 없이 검사

### 16. 책 읽기 콘텐츠 (data/books/*.json)
- XOR 암호화 (키: `chaeksoop2024`)
- Base64 → XOR 복호화 → JSON 파싱
- 구조: `{ "chapters": [{ "title": "...", "paragraphs": ["...", "img:url", ...] }] }`
- 이미지: `img:url` 형식, reader에서 `<div class="reader-image-wrap"><img></div>`로 변환
- 7권만 존재 (id: 1,2,3,38,42,46,47)
- 미준비 도서: `이 책의 읽기 콘텐츠를 준비 중입니다.` alert

---

## Firebase / 데이터

### Firebase 설정
```
firebase.initializeApp({
  apiKey: "AIzaSyCCCY6sRrqBTBSYg6g1aRjnW8dN7obldW8",
  authDomain: "chaeksoop.firebaseapp.com",
  projectId: "chaeksoop",
  storageBucket: "chaeksoop.firebasestorage.app",
  messagingSenderId: "134266719032",
  appId: "1:134266719032:web:66e02d85b9d178ba3e806b"
})
const db = firebase.firestore()
```

### Firestore 컬렉션
| 컬렉션 | 문서 ID | 주요 필드 | 사용 |
|--------|---------|-----------|------|
| `reviews` | auto | `bookId`, `name`, `text`, `email`, `createdAt`, `approved`, `event` | 리뷰/기대평 |
| `messages` | auto | `name`, `text`, `contact`, `createdAt` | 부스 메시지 |

### Firestore 규칙 (`firestore.rules`)
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /reviews {
      allow read: if true;
      allow create: if request.resource.data.keys().hasAll(['id','bookId','text','createdAt'])
                     && request.resource.data.text is string
                     && request.resource.data.text.size() < 500
                     && request.resource.data.name is string
                     && request.resource.data.name.size() < 20
                     && request.resource.data.bookId is number
                     && request.resource.data.event is bool
                     && request.resource.data.approved == true;
      allow delete, update: if false;
    }
    match /messages {
      allow read: if true;
      allow create: if request.resource.data.keys().hasAll(['id','text'])
                     && request.resource.data.text is string
                     && request.resource.data.text.size() < 500
                     && request.resource.data.name is string
                     && request.resource.data.name.size() < 20;
      allow delete, update: if false;
    }
    match /{document=**} { allow read, write: if false; }
  }
}
```
**주의**: Firebase Console에서 수동 배포 필요 (`firebase deploy --only firestore:rules` 또는 Console 붙여넣기)

### XOR 암호화
- 키: `chaeksoop2024`
- 목적: 콘텐츠 보호보다 우발적 접근 방지 (보안 아님)
- 미암호화 원본: `ebook-content.json` (~500KB, root + data/ 두 곳)

---

## 보안

### 적용 완료
- XSS 방어: `escapeHtml()`로 모든 사용자 입력 렌더링 (DOM textContent 방식)
- 프로토타입 오염: `{...d.data()}` → 명시적 필드 추출
- 인라인 onclick 제거 → `addEventListener`
- catch 블록: 전부 `console.error` 로깅
- Reader null 체크: `chapters`, `paragraphs` 안전 접근
- Mailto: `encodeURIComponent` 적용
- 중복 리뷰 방지: Firestore `where('name','==',name).where('text','==',text).get()` 쿼리
- 이중 submit 제거: delegation만 사용
- 복사 방지: user-select + 5개 이벤트 차단
- Admin 패널 완전 제거
  - 과거: 로고 5회 클릭 → 암호입력(`lkjh11`, SHA-256: `f7a4368b1d02b33a2c56979c09392aa47a521518505e0918959a3f147bf68242`)
  - 현재: 승인/삭제/내보내기 기능 모두 제거 (-363줄)
  - 리뷰는 auto-approve (approved: true)
  - 관리자는 Firebase Console에서 직접 작업

### 미해결 (Firebase Console 필요)
- **CRITICAL**: Firestore 규칙 미배포 (현재 누구나 read/write 가능)
- **HIGH**: 관리자 인증 없음 (클라이언트 측 암호 제거됨)
- **MEDIUM**: 이메일 평문 저장 (raw email in Firestore)

---

## UI/UX 상세

### 디자인 시스템
| 요소 | 값 |
|------|-----|
| 폰트 | Pretendard, -apple-system, BlinkMacSystemFont, sans-serif |
| 배경색 | `#EEF3EC` (연한 녹회색) |
| 본문색 | `#2C3E2D` (진한 녹색) |
| 포인트색 | `#A8C9A5` (따뜻한 연두) |
| 오버레이 | `rgba(30,50,30,0.5)` + blur(북팝업) / `rgba(44,62,45,0.3~0.4)`(기타) |
| 카드 | `#fff`, border-radius 16px, 그림자 |
| 리더 배경 | `#F5F0E8` (종이톤) |
| 뱃지 | orange gradient `#FFB347→#FF8C47` (이벤트) |
| 버튼 | green gradient `#6B9E78→#5A8E66` |
| 강조 버튼 | gold `#D4A853→#C49A48` (다음읽기/완료) |

### 반응형
| 기준 | 대상 | 변경점 |
|------|------|--------|
| `768px↑` | 태블릿+ | container 640→720px, 북리스트 1열→2열 grid, FAB 원형→필형, header 패딩 증가 |
| `480px↓` | 작은폰 | 리뷰 슬라이드 폰트/패딩 축소, 캐러셀 높이 48→44px |
| `480px↑` | 중간폰 | event-notice 패딩 10×12→16×20 |

### Z-index 레이어 (낮음→높음)
`0` 푸터 장식 → `1` 컨테이너/헤더/칩/이벤트박스/북카드 → `2` 카드액센트/캐러셀페이드 → `9` 진행바 → `10` 리더헤더/넥스트챕터 → `160~161` 메시지모달 → `170~171` 칩모달 → `900` 북팝업 → `1500` 플로팅버튼 → `1700~1800` 스탑드로어 → `2000` 리더 → `3000` 컴플리션 → `3100~3101` 리뷰성공/리스트

### 애니메이션
| 이름 | 대상 | 지속시간 | 효과 |
|------|------|----------|------|
| popupSlideUp | 팝업들 | 0.35s | translateY(30)+scale(0.95)→(0) |
| drawerSlideUp | 스탑드로어 | 0.3s | translateY(100%)→0 |
| chipsFadeIn | 칩모달 | 0.2s | scale(0.92)→1 |
| msgFadeIn | 메시지모달 | 0.25s | scale(0.95)→1 |
| carouselScroll | 커버캐러셀 | 60s linear infinite | translateX(0)→-50% |
| timerPulse | 타이머(완료시) | 1s ease infinite | opacity 1→0.6 |
| badgePop | 이벤트뱃지 | 순간 | scale 0→1.2→1 |

### 캐러셀 자동 스크롤
- 기본: CSS `carouselScroll` 60s linear infinite
- 드래그 시: JS `requestAnimationFrame` 0.4px/frame (drag 중단 시 일시정지)
- 드래그 종료 4초 후 재개

---

## 파일 인벤토리

### 핵심 파일
| 파일 | 크기 | 설명 |
|------|------|------|
| `index.html` | ~95KB | 전체 앱 (HTML + JS 인라인, 2462줄) |
| `css/style.css` | ~47KB | 모든 스타일 (2578줄) |
| `data/books/{1,2,3,38,42,46,47}.json` | 15KB~465KB | XOR 암호화된 본문 (7개) |
| `images/*` | ~11MB | 47권 표지 + 로고 + 40장 backyard 이미지 |
| `firestore.rules` | 1.2KB | Firestore 보안 규칙 |
| `firebase.json` | 56B | Firebase 설정 |
| `scrape_culturlook.py` | 14KB | 알라딘 크롤러 |
| `ebook-content.json` | ~500KB | 미암호화 책 본문 (root) |
| `AGENTS.md` | — | 이 파일 |

### 이미지 상세 (`images/`)
- 47권 표지: `cl_*.jpg`(42개, 컬처룩) + `creative-act.jpg` `backyard-birds.jpg` `ways-of-being.jpg` `forever-dog.jpg` `forever-dog-life.jpg` `healing-the-mind.jpg` `our-way-of-living.jpg` `world-by-chance.jpg` `cl_ai_calc.jpg/svg`
- 로고: `logo.png`(692KB) `culturelook.png`(11KB) `cocoon.png`(11KB)
- Backyard 내부: `backyard/p0008.jpg~p0452.jpg` (40장)
- 책 18 `The Marvelous Clouds` 표지 없음 (image="" → initials fallback)

### 이전 버전 보존
- `book-forest/` — 초기 버전 전체
- `book-forest-v5/` — v5 버전

---

## 주요 의사결정
- CSP `<meta>` 태그 제외: Firebase connect-src 도메인을 전부 명시할 수 없어 기능 차단 위험
- IIFE 래핑 제외: 전역 함수 참조 깨짐 방지 (createBookCard 등 동적 HTML에서 호출)
- SHA-256 폴백 제거: 관리자 기능 자체를 제거하여 불필요
- XOR 암호화: 콘텐츠 보호보다 우발적 접근 방지 목적 (보안 아님)
- Firebase Auth 도입 없음: Firestore 규칙만으로 방어
- 일반/이벤트 리뷰 동일 Firestore `reviews` 컬렉션, `bookId`+`event` 필드로 구분
- 리뷰 auto-approve: 관리자 패널이 없으므로 모든 리뷰 즉시 승인
- Confetti: 이벤트 도서 성공 팝업에만 표시
- 뒤로가기: 모든 오버레이를 popstate로 통합 관리 (개별 close 함수 중복 호출 가능)

## 외부 의존성
- Pretendard 폰트 (Google Fonts)
- Firebase Firestore compat SDK v10.14.1 (`@firebase/firestore` / `firebase-firestore-compat`)
- SheetJS (`xlsx`) — 엑셀 다운로드

## 알려진 이슈 / TODO
- **CRITICAL**: Firestore 보안 규칙 미배포 (Console에서 Publish 필요)
- `data/books/`에 47권 중 7권만 존재 (1,2,3,38,42,46,47) — 나머지 40권은 읽기 콘텐츠 없음
- 관리자 삭제 필요 시 Firebase Console에서 직접 문서 삭제
- Cloud Functions rate limit 없어 스크립트 대량 등록 위험 (행사 기간 짧아 위험 낮음)
- Popup `animation: popupSlideUp`이 cover carousel과 review carousel에도 동일 이름으로 중복 선언됨 (의도적, 동일 동작)
