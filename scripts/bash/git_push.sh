#!/bin/bash
MSG="${1:-auto: cambios del $(date +%Y-%m-%d)}"
cd ~/devops
git add .
git commit -m "$MSG"
git push
echo "✓ Push completado: $MSG"
