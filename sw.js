/* 뿌리 오프라인 지원 (한국어판 / 와 영어판 /en/ 공용).
   카드나 화면을 고치면 CACHE 이름의 숫자를 올려야 설치한 폰에도 새 버전이 확실히 반영된다. */
const CACHE = 'ppuri-v7';
const FONTS = 'ppuri-fonts';
const CORE = [
  './',
  'index.html',
  'manifest.webmanifest',
  'en/',
  'en/index.html',
  'en/manifest.webmanifest',
  'icons/icon-192.png',
  'icons/icon-512.png',
  'icons/icon-maskable-512.png',
  'icons/apple-touch-icon.png',
  'icons/favicon.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith('ppuri-') && k !== CACHE && k !== FONTS).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // 앱 화면: 온라인이면 새 버전, 오프라인이면 그 주소로 저장해 둔 버전
  if (req.mode === 'navigate') {
    const key = new URL(url.href); key.search = ''; key.hash = '';
    const isEn = /\/en\/?(index\.html)?$/.test(key.pathname);
    e.respondWith(
      fetch(req)
        .then(res => {
          if (res.ok && res.type === 'basic') { const copy = res.clone(); caches.open(CACHE).then(c => c.put(key.href, copy)); }
          return res;
        })
        .catch(async () =>
          (await caches.match(key.href)) ||
          (await caches.match(isEn ? 'en/index.html' : 'index.html')) ||
          caches.match(isEn ? 'en/' : './'))
    );
    return;
  }

  // 글꼴: 저장본을 먼저 쓰고 뒤에서 갱신
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(caches.open(FONTS).then(async c => {
      const hit = await c.match(req);
      const net = fetch(req).then(res => {
        if (res.ok || res.type === 'opaque') c.put(req, res.clone());
        return res;
      }).catch(() => hit);
      return hit || net;
    }));
    return;
  }

  // 아이콘 등 같은 사이트 파일: 저장본 우선
  if (url.origin === self.location.origin) {
    e.respondWith(caches.match(req, { ignoreSearch: true }).then(hit => hit || fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    })));
  }
});
