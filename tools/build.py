"""뿌리 빌드: src/app.html 템플릿 하나로 한국어판(index.html)과 영어판(en/index.html)을 만든다.

사용법:
  python3 tools/build.py                 # index.html, en/index.html, en/manifest.webmanifest
  python3 tools/build.py --preview OUT   # Claude 미리보기용 한국어판 한 장(헤드 없이)도 만든다

입력:
  src/app.html       화면, 코드, 한국어 카드 데이터(C_KO), 퀴즈 어휘(V)
  src/strings.json   화면 문구 (ko, en)
  content/en.json    영어 카드 문구 (카드 id → h, m, roman, skip)
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REDIRECT_KO = ("<script>try{if(!window.PPURI_PREVIEW){var p=localStorage.getItem('ppuri-lang');"
               "var ls=((navigator.languages&&navigator.languages.length)?navigator.languages:[navigator.language||'']).join(',').toLowerCase();"
               "if(p==='en'||(p!=='ko'&&ls.indexOf('ko')<0)){location.replace('en/'+location.search+location.hash);}}}catch(e){}</script>")

EN_MANIFEST = {
    "name": "Ppuri: word family trees",
    "short_name": "Ppuri",
    "description": "One surprising line per card: swipe through the family trees of everyday words.",
    "lang": "en",
    "dir": "ltr",
    "id": "./",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#E9EDE6",
    "theme_color": "#E9EDE6",
    "categories": ["education", "books"],
    "icons": [
        {"src": "../icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "../icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "../icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}


def js_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def render(template, strings, en_data, loc):
    other = 'en' if loc == 'ko' else 'ko'
    vars_ = {
        'lang': loc,
        'base': '' if loc == 'ko' else '../',
        'otherHref': 'en/' if loc == 'ko' else '../',
        'otherLang': other,
        'redirect': REDIRECT_KO if loc == 'ko' else '',
        'STR_JSON': js_json(strings[loc]),
        'EN_JSON': js_json(en_data) if loc == 'en' else 'null',
    }
    out = template
    for k, v in vars_.items():
        out = out.replace('{{' + k + '}}', v)
    for k, v in strings[loc].items():
        out = out.replace('{{' + k + '}}', html.escape(v, quote=True))
    left = re.findall(r'\{\{[A-Za-z_]+\}\}', out)
    assert not left, f'unfilled placeholders in {loc}: {sorted(set(left))}'
    return out


def preview(ko_html):
    """Claude 아티팩트 미리보기용: 문서 골격과 PWA 헤드를 빼고, 통계·서비스워커·리다이렉트를 끈다."""
    a = ko_html
    for t in ['<!doctype html>\n', '<html lang="ko">\n', '<head>\n', '</head>\n', '<body>\n', '</body>\n', '</html>\n',
              '<meta charset="utf-8">\n', '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n']:
        assert a.count(t) == 1, t
        a = a.replace(t, '')
    a = re.sub(r'<meta name="theme-color"[^>]*>\n|<link rel="(manifest|icon|apple-touch-icon|alternate)"[^>]*>\n|'
               r'<meta name="(apple-mobile-web-app-[a-z-]+|mobile-web-app-capable)"[^>]*>\n', '', a)
    a = a.replace(REDIRECT_KO + '\n', '')
    a = '<script>window.PPURI_PREVIEW = true;</script>\n' + a
    return a


def main():
    template = open(os.path.join(ROOT, 'src/app.html'), encoding='utf-8').read()
    strings = json.load(open(os.path.join(ROOT, 'src/strings.json'), encoding='utf-8'))
    en_data = json.load(open(os.path.join(ROOT, 'content/en.json'), encoding='utf-8'))
    assert set(strings['ko']) == set(strings['en']), set(strings['ko']) ^ set(strings['en'])

    ko = render(template, strings, en_data, 'ko')
    en = render(template, strings, en_data, 'en')
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(ko)
    os.makedirs(os.path.join(ROOT, 'en'), exist_ok=True)
    open(os.path.join(ROOT, 'en/index.html'), 'w', encoding='utf-8').write(en)
    with open(os.path.join(ROOT, 'en/manifest.webmanifest'), 'w', encoding='utf-8') as fh:
        json.dump(EN_MANIFEST, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    print('built index.html, en/index.html, en/manifest.webmanifest')

    if '--preview' in sys.argv:
        out = sys.argv[sys.argv.index('--preview') + 1]
        open(out, 'w', encoding='utf-8').write(preview(ko))
        print('preview', out)


if __name__ == '__main__':
    main()
