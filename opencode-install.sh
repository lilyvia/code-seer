#!/bin/bash

rm -rf ~/.config/opencode/skills/code-seer
mkdir -p ~/.config/opencode/skills/code-seer
rsync -av --delete SKILL.md ~/.config/opencode/skills/code-seer/
rsync -av --delete references ~/.config/opencode/skills/code-seer/

find ~/.config/opencode/skills/code-seer -type d -exec chmod 755 {} \;
find ~/.config/opencode/skills/code-seer -type f -exec chmod 644 {} \;
