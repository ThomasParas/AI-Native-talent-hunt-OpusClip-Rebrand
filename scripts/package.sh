#!/usr/bin/env bash
# Builds opusclip-rebrand-submission.zip + extra uploads into dist/upload/. Only touches dist/upload and the staging dir.
set -euo pipefail
cd "$(dirname "$0")/.."
UP=dist/upload; STAGE=dist/stage
rm -rf "$UP" "$STAGE"; mkdir -p "$UP" "$STAGE/page"
cp dist/rebrand-thesis.pdf dist/proof-of-concept-page.pdf README.md "$STAGE/"
cp page/index.html "$STAGE/page/"
(cd "$STAGE" && zip -qr -X ../upload/opusclip-rebrand-submission.zip .)
cp docs/PROCESS.md "$UP/PROCESS.md"
echo "https://github.com/ThomasParas/AI-Native-talent-hunt-OpusClip-Rebrand" > "$UP/repo-link.txt"
rm -rf "$STAGE"
unzip -l "$UP/opusclip-rebrand-submission.zip"; ls -la "$UP"
