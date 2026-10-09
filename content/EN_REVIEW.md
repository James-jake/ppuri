# Ppuri English edition: review spec

You are an independent reviewer. You did not write these English cards. Read `/home/claude/ppuri/content/EN_SPEC.md` first: it is the brief the translator followed.

For each card in your English file, compare it with the Korean source card (same id) in `/home/claude/ppuri/content/cards_ko.json`, and check:

1. **Fact drift (most important).** The English must make exactly the same claims as the Korean: no added facts, dates, names or glosses; nothing dropped that changes the meaning; hedges exactly as strong ("the leading theory", "probably", "no one knows", "a popular story but…"). If the Korean itself contains a claim that is plainly wrong or overstated in a way the English made more visible, fix the English to the defensible version and note it in your log so the Korean can be fixed too.
2. **Reads naturally to a native US English speaker.** Short, punchy hooks; friendly plain sentences. Rewrite anything clunky or translated-sounding.
3. **Quote rule.** If the hook has curly single quotes ‘…’, the LAST quoted phrase is the reveal a quiz will blank out, and it is ≤ 24 characters. If the last quoted phrase is not something a reader could recall as "the answer", rewrite so it is.
4. **Lengths.** hook ≤ 52 chars, reason ≤ 170 chars.
5. **Romanization.** Korean/Hanja strip words use Revised Romanization (pronunciation-based: 덕률풍 → deongnyulpung).
6. **Skips.** Skipped cards should be ones that only work if you read Korean. If a skipped card could clearly work for an English reader, you may un-skip it by writing `h`, `m`, `roman`.

Edit your English file in place. Keep its JSON shape. Do not touch other files except your log.

Write a log to the log file you're given: one line per changed card id with what changed and why. Unchanged cards are not listed.

Run a node check at the end (parses, ids unchanged, lengths, last-quote ≤ 24, roman present for Korean/Hanja words on non-skipped cards).

Final message: cards checked, cards changed, the three most important fixes, and any Korean card that should be corrected.
