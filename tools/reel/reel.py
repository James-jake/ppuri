"""뿌리 카드를 인스타 릴스용 세로 영상(1080x1920, 8초, 무음)으로 만든다.

준비:  bash tools/reel/get_fonts.sh
사용:  python3 tools/reel/reel.py --lang en --ids bd-muscle,vodka --out OUTDIR [--theme-start 0]

카드 문구는 content/cards_ko.json(한국어)과 content/en.json(영어)에서 읽는다.
글자가 넘치면 훅·설명·단어 크기를 자동으로 줄인다. 음악은 인스타 앱에서 붙인다.
"""
import argparse, html, json, os, shutil, subprocess, tempfile
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FONTS = os.path.join(HERE, 'fonts')
FPS, SECONDS = 30, 8
THEMES = [
    {'bg': '#1E3A2F', 'ink': '#EEF2EA', 'acc': '#E8B04A'},
    {'bg': '#22407E', 'ink': '#F1F3FA', 'acc': '#F4C95D'},
    {'bg': '#E4AE45', 'ink': '#20190C', 'acc': '#5A2A10'},
    {'bg': '#5E1F38', 'ink': '#F7ECEF', 'acc': '#F2B6C8'},
    {'bg': '#DCE4D4', 'ink': '#18231E', 'acc': '#22407E'},
    {'bg': '#2E2A4F', 'ink': '#EEEAF7', 'acc': '#9FD8C8'},
]
BRAND = {'ko': ('뿌리', 'james-jake.github.io/ppuri'), 'en': ('Ppuri', 'james-jake.github.io/ppuri/en')}
LANG_EN = {'영어': 'English', '독일어': 'German', '프랑스어': 'French', '스페인어': 'Spanish', '이탈리아어': 'Italian',
           '포르투갈어': 'Portuguese', '네덜란드어': 'Dutch', '러시아어': 'Russian', '일본어': 'Japanese', '중국어': 'Chinese',
           '한국어': 'Korean', '한자': 'Hanja', '라틴어': 'Latin', '그리스어': 'Greek', '고대영어': 'Old English',
           '중세영어': 'Middle English', '고대노르드어': 'Old Norse', '고대독일어': 'Old High German', '산스크리트어': 'Sanskrit',
           '페르시아어': 'Persian', '아랍어': 'Arabic', '튀르키예어': 'Turkish', '힌디어': 'Hindi', '나와틀어': 'Nahuatl', '체코어': 'Czech'}

FIT_JS = """() => {
  const body = document.querySelector('.body');
  const hook = document.querySelector('.hook'), more = document.querySelector('.more');
  const ws = [...document.querySelectorAll('.w')];
  body.style.justifyContent = 'flex-start';
  const over = () => body.scrollHeight - body.clientHeight;
  for (const h of [100, 92, 84, 78, 72]) { hook.style.fontSize = h + 'px'; if (over() <= 0) break; }
  for (const m of [42, 40, 38, 36, 34]) { if (over() <= 0) break; more.style.fontSize = m + 'px'; }
  for (const w of [60, 56, 52, 48]) { if (over() <= 0) break; ws.forEach(x => x.style.fontSize = w + 'px'); }
  const left = over();
  body.style.justifyContent = '';
  return left;
}"""


def load_cards(lang):
    ko = {c['id']: c for c in json.load(open(os.path.join(ROOT, 'content/cards_ko.json'), encoding='utf-8'))}
    if lang == 'ko':
        return {i: (c['e'], c['h'], [(w, l, p) for w, l, p in c['s']], c['m']) for i, c in ko.items()}
    en = json.load(open(os.path.join(ROOT, 'content/en.json'), encoding='utf-8'))
    out = {}
    for i, c in ko.items():
        t = en.get(i)
        if not t or t.get('skip'):
            continue
        strip = []
        for w, l, p in c['s']:
            if l in ('한국어', '한자'):
                p = (t.get('roman') or {}).get(w, '')
            strip.append((w, LANG_EN.get(l, l), p))
        out[i] = (c['e'], t['h'], strip, t['m'])
    return out


def page_html(card, theme, lang):
    emoji, hook, strip, more = card
    brand, url = BRAND[lang]
    e = html.escape
    rows = ''.join(
        f'<div class="row" style="--i:{i}"><div class="w">{e(w)}{f"<span class=ipa>{e(p)}</span>" if p else ""}</div>'
        f'<div class="l">{e(l)}</div></div>' for i, (w, l, p) in enumerate(strip))
    n = len(strip)
    t = theme
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>
@font-face{{font-family:H;src:url(Hahmlet.ttf)}}
@font-face{{font-family:P;src:url(IBMPlexSansKR-Regular.ttf);font-weight:400}}
@font-face{{font-family:P;src:url(IBMPlexSansKR-Medium.ttf);font-weight:500}}
@font-face{{font-family:E;src:url(NotoColorEmoji.ttf)}}
:root{{--bg:{t['bg']};--ink:{t['ink']};--acc:{t['acc']}}}
*{{box-sizing:border-box;margin:0}}
html,body{{width:1080px;height:1920px;background:var(--bg);color:var(--ink);overflow:hidden}}
/* 인스타 릴스 UI가 덮는 곳(위 ~220px, 아래 ~340px, 오른쪽 ~140px)을 피한다 */
.wrap{{position:absolute;left:96px;right:150px;top:236px;bottom:360px;display:flex;flex-direction:column}}
.brand{{display:flex;align-items:baseline;gap:20px;font:500 34px P;opacity:.75}}
.brand b{{font:800 44px H;letter-spacing:-.02em}}
.body{{flex:1;min-height:0;overflow:hidden;display:flex;flex-direction:column;justify-content:center}}
.emo{{font:104px E;line-height:1;margin-bottom:34px}}
.hook{{font:800 100px/1.2 H, "Noto Serif CJK KR", serif;letter-spacing:-.025em;word-break:keep-all;overflow-wrap:break-word}}
.rule{{height:5px;background:var(--acc);margin:44px 0 10px;transform-origin:left;animation:grow .5s cubic-bezier(.2,.7,.2,1) .9s both}}
.row{{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:18px 0;
  border-bottom:2px solid color-mix(in srgb,var(--ink) 16%,transparent);
  animation:rise .42s cubic-bezier(.2,.7,.2,1) calc(1.25s + var(--i)*.38s) both}}
.w{{font:600 60px/1.2 H, "Noto Serif CJK KR", serif;display:flex;align-items:baseline;gap:22px;flex-wrap:wrap;min-width:0}}
.ipa{{font:400 34px P;opacity:.8}}
.l{{font:400 30px P;opacity:.7;white-space:nowrap}}
.more{{font:400 42px/1.55 H, "Noto Serif CJK KR", serif;margin-top:36px;word-break:keep-all;animation:fade .55s ease {1.25 + n * 0.38 + 0.45:.2f}s both}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(26px)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
</style></head><body><div class="wrap">
<div class="brand"><b>{e(brand)}</b><span>{e(url)}</span></div>
<div class="body"><div class="emo">{e(emoji)}</div><div class="hook">{e(hook)}</div>
<div class="rule"></div>{rows}<p class="more">{e(more)}</p></div>
</div></body></html>'''


def render(card, theme, lang, out_mp4):
    work = tempfile.mkdtemp(prefix='reel-')
    try:
        for f in os.listdir(FONTS):
            os.symlink(os.path.join(FONTS, f), os.path.join(work, f))
        with open(os.path.join(work, 'r.html'), 'w', encoding='utf-8') as fh:
            fh.write(page_html(card, theme, lang))
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
            pg.goto('file://' + os.path.join(work, 'r.html'))
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(300)
            left = pg.evaluate(FIT_JS)
            for i in range(FPS * SECONDS):
                pg.evaluate(f"document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {i * 1000 / FPS}; }})")
                pg.screenshot(path=os.path.join(work, f'f{i:04d}.png'))
            b.close()
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(work, 'f%04d.png'),
                        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium',
                        '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', out_mp4], check=True)
        shutil.copy(os.path.join(work, 'f0000.png'), out_mp4.replace('.mp4', '_cover.png'))
        shutil.copy(os.path.join(work, f'f{FPS * SECONDS - 1:04d}.png'), out_mp4.replace('.mp4', '_end.png'))
        return left
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lang', choices=['ko', 'en'], default='en')
    ap.add_argument('--ids', required=True, help='comma-separated card ids, in posting order')
    ap.add_argument('--out', required=True)
    ap.add_argument('--theme-start', type=int, default=0)
    ap.add_argument('--number-from', type=int, default=1)
    a = ap.parse_args()
    cards = load_cards(a.lang)
    os.makedirs(a.out, exist_ok=True)
    for k, cid in enumerate(a.ids.split(',')):
        n = a.number_from + k
        out = os.path.join(a.out, f'{n:02d}_{cid}.mp4')
        left = render(cards[cid], THEMES[(a.theme_start + n - 1) % len(THEMES)], a.lang, out)
        print(f'{os.path.basename(out)} overflow={left}', flush=True)


if __name__ == '__main__':
    main()
