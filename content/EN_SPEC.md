# Ppuri English edition: card writing spec

Ppuri ("뿌리", Korean for "root") is a reels-style etymology app: one card per screen, one surprising line, a few related words in several languages, and a one-to-two sentence reason that appears when the reader taps. The Korean edition already has 305 fact-checked cards. You are writing the **English edition** of a batch of them for curious general readers in the US and worldwide.

This is rewriting, not literal translation. The English line must make an English reader stop scrolling, just as the Korean one does for a Korean reader. But the **facts must stay exactly as they are**: the Korean cards were fact-checked against Etymonline, Wiktionary, DWDS, Kotobank and the Korean national dictionary, and you must not add, remove or change any claim.

## Input
A JSON array of cards: `{id, e, h, s, m}`
- `h`: the Korean hook line
- `s`: the word strip, `[word, language (in Korean), pronunciation]`
- `m`: the Korean reason (shown on tap)

Language names you will see: 영어 English, 독일어 German, 프랑스어 French, 스페인어 Spanish, 이탈리아어 Italian, 포르투갈어 Portuguese, 네덜란드어 Dutch, 러시아어 Russian, 일본어 Japanese, 중국어 Chinese, 한국어 Korean, 한자 Hanja (Chinese characters as used in Korean), 라틴어 Latin, 그리스어 Greek, 고대영어 Old English, 중세영어 Middle English, 고대노르드어 Old Norse, 고대독일어 Old High German, 산스크리트어 Sanskrit, 페르시아어 Persian, 아랍어 Arabic, 튀르키예어 Turkish, 힌디어 Hindi, 나와틀어 Nahuatl, 체코어 Czech.

## Output
Write one JSON object to the output file you are given, keyed by card id:

```json
{
  "vodka":  {"h": "Vodka literally means ‘little water’", "m": "Russian voda (water) plus a suffix meaning small. Voda shares a root with English water."},
  "bread":  {"h": "Korean ‘ppang’ (bread) is a Portuguese word", "m": "...", "roman": {"빵": "ppang"}},
  "bd-garak": {"skip": true, "why": "Depends on Korean spelling: 손가락/젓가락 share the native word 가락."}
}
```

Include **every** card id from your input, either translated or skipped.

### `h` — the hook
- At most **52 characters** including spaces. Shorter is better.
- Sentence case, no period at the end. A question is fine.
- Keep the surprise. Lead with the familiar word, end on the reveal.
- **Quote rule (the quiz depends on it):** if the Korean hook has a phrase in curly single quotes ‘…’, the English hook must also put its key reveal in curly single quotes ‘…’ (U+2018 / U+2019, not straight quotes), and the **last** quoted phrase must be the reveal. Keep that quoted phrase **24 characters or fewer**. Do not use curly single quotes for anything else in the hook (use double quotes “…” or italics-free plain text for word mentions). If the Korean hook has no ‘…’, you may add one around the reveal if it reads naturally, but don't force it.
- Mention foreign words in plain text (vodka, Schule). Mention Korean words in romanization, optionally with Hangul: ppang, or ppang (빵).

### `m` — the reason
- One or two sentences, at most **170 characters**.
- Plain, friendly American English. US spelling.
- Keep every hedge exactly as strong as the Korean: 설이 유력해요 = "the leading theory is" / "probably"; 확실하지 않아요 = "no one knows for sure" / "it's uncertain"; 속설/민간어원 = "a popular story, but…". Never turn a hedged claim into a certain one, or the reverse.
- Keep dates, names and numbers exactly. Do not add new ones.
- Where the Korean explains something English speakers already know (for example what an English word means), drop that part and keep the etymology.

### `roman` — Korean and Hanja words in the strip
For every strip item whose language is 한국어 or 한자, give its Korean reading in Revised Romanization (the official South Korean system: 빵 → ppang, 남편 → nampyeon, 歌手 → gasu). Key = the word exactly as it appears in the strip.

### `skip`
Skip a card (`{"skip": true, "why": "..."}`) when the surprise only works if you can read Korean: Korean spelling or sound changes (머리카락, 숟가락), the history of a native Korean word, wordplay in Hangul, or a fact about how Koreans use a word that means nothing to an outsider.

Keep (do not skip) cards about Chinese characters, Japanese, loanword journeys, or anything an English reader can follow from the strip words plus your sentence. "Korean ‘ppang’ (bread) came from Portuguese via Japan" is a keeper; it is a fun fact about Korean for an English reader.

Expect to skip roughly 10–20% of cards with Korean or Hanja in the strip, and almost none of the others.

## Before you finish
Run a quick node check on your file: it parses, every input id appears exactly once, `h` ≤ 52 chars, `m` ≤ 170 chars, the last ‘…’ in `h` is ≤ 24 chars, every Korean/Hanja strip word on a non-skipped card has a `roman` entry. Fix anything that fails.

Final message: number translated, number skipped (with the ids), and any card where you weren't sure the English kept the meaning. Do not paste the file.
