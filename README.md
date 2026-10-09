# 뿌리 / Ppuri

한 장에 한 줄씩 넘겨 보는 어원 카드 앱. 하루 10장.

- 한국어판 (카드 305장): https://james-jake.github.io/ppuri/
- 영어판 (카드 294장): https://james-jake.github.io/ppuri/en/

폰 언어 목록에 한국어가 없으면 첫 화면에서 영어판으로 넘어간다. 오른쪽 위 언어 버튼을 한 번 누르면 그 선택을 기억한다.

## 설치
- 안드로이드 크롬: 화면 위쪽 "앱 설치" 버튼, 또는 메뉴 → 홈 화면에 추가
- 아이폰 Safari: 아래쪽 공유 버튼 → 홈 화면에 추가 (카카오톡·인스타 안의 브라우저에서는 안 되니 Safari로 열기)

## 파일 구성
```
src/app.html           화면·코드·한국어 카드(C_KO)·퀴즈 어휘(V) — 원본 템플릿
src/strings.json       화면 문구 (ko, en)
content/en.json        영어 카드 문구 (카드 id → h, m, roman, skip)
tools/build.py         원본으로 아래 두 파일을 만든다
index.html             한국어판 (빌드 결과, 직접 고치지 말 것)
en/index.html          영어판 (빌드 결과, 직접 고치지 말 것)
en/manifest.webmanifest
manifest.webmanifest   한국어판 앱 정보
sw.js                  오프라인 지원 (두 언어 공용)
icons/                 홈 화면 아이콘
content/               카드 원본, 작성·번역·검수 규칙과 기록
```

## 고치거나 카드를 늘릴 때
1. `src/app.html`(한국어 카드·코드), `src/strings.json`(문구), `content/en.json`(영어 카드)을 고친다.
2. `python3 tools/build.py` 로 `index.html`과 `en/index.html`을 다시 만든다.
3. `sw.js` 맨 위 `CACHE` 숫자를 하나 올린다. 그래야 설치한 폰에도 새 버전이 반영된다.
4. `main`에 올리면 1~2분 뒤 GitHub Pages에 반영된다.

규칙: 한국어 카드 작성은 `content/SPEC.md`, 검수는 `content/REVIEW.md`, 영어 번역은 `content/EN_SPEC.md`, 영어 검수는 `content/EN_REVIEW.md`.

## 방문 통계
GoatCounter(쿠키 없음): https://kjake.goatcounter.com
이벤트: `day-complete`, `quiz-right`, `quiz-wrong`, `review-start`, `share`, `install` (영어판은 앞에 `en-`)
채널 구분 링크: 주소 뒤에 `?ref=instagram`, `?ref=threads`, `?ref=x`
