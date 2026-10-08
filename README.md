# 뿌리

한 장에 한 줄씩 넘겨 보는 어원 카드 앱. 하루 10장, 카드 305장.

**바로 열기:** https://james-jake.github.io/ppuri/

## 설치
- 안드로이드 크롬: 화면 위쪽 "앱 설치" 버튼, 또는 메뉴 → 홈 화면에 추가
- 아이폰 Safari: 아래쪽 공유 버튼 → 홈 화면에 추가 (카카오톡·인스타 안의 브라우저에서는 안 되니 Safari로 열기)

## 파일 구성
```
index.html             앱 전체 (카드 데이터 포함)
manifest.webmanifest   앱 이름, 아이콘, 전체 화면 설정
sw.js                  오프라인 지원
icons/                 홈 화면 아이콘
content/               카드 원본(JSON)과 작성·검수 기록
```

## 카드를 고치거나 늘릴 때
1. `content/`의 원본을 고친 뒤 `index.html`의 카드 데이터(`const C`, `const V`)에 반영한다.
2. `sw.js` 맨 위의 `CACHE` 이름 숫자를 하나 올린다 (`ppuri-v4` → `ppuri-v5`). 그래야 이미 설치한 폰에도 새 버전이 확실히 반영된다.
3. `main`에 올리면 1~2분 뒤 GitHub Pages에 반영된다.

카드 작성 규칙은 `content/SPEC.md`, 검수 규칙은 `content/REVIEW.md`에 있다.
