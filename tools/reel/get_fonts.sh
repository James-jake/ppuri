#!/usr/bin/env bash
# 릴스 렌더링용 글꼴을 tools/reel/fonts/ 에 받는다 (저장소에는 올리지 않음).
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)/fonts"
mkdir -p "$D" && cd "$D"
[ -f Hahmlet.ttf ] || curl -sSL -o Hahmlet.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/hahmlet/Hahmlet%5Bwght%5D.ttf"
if [ ! -f IBMPlexSansKR-Regular.ttf ]; then
  curl -sSL -o plex.zip "https://github.com/IBM/plex/releases/download/%40ibm%2Fplex-sans-kr%401.1.0/ibm-plex-sans-kr.zip"
  unzip -o -j -q plex.zip "ibm-plex-sans-kr/fonts/complete/ttf/unhinted/IBMPlexSansKR-Regular.ttf" "ibm-plex-sans-kr/fonts/complete/ttf/unhinted/IBMPlexSansKR-Medium.ttf"
  rm plex.zip
fi
[ -f NotoColorEmoji.ttf ] || cp /usr/share/fonts/truetype/noto/NotoColorEmoji.ttf . 2>/dev/null || curl -sSL -o NotoColorEmoji.ttf "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/fonts/NotoColorEmoji.ttf"
ls -la
