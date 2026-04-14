#!/bin/bash

rm -rf ~/.config/opencode/skills/security-audit
[ -d ~/.config/opencode/skills/security-audit ] && mkdir ~/.config/opencode/skills/security-audit
rsync -av --delete SKILL.md ~/.config/opencode/skills/security-audit/
rsync -av --delete references ~/.config/opencode/skills/security-audit/

find ~/.config/opencode/skills/security-audit -type d -exec chmod 755 {} \;
find ~/.config/opencode/skills/security-audit -type f -exec chmod 644 {} \;
