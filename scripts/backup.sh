#!/bin/bash
ORIGEN="$HOME/devops/scripts"
DESTINO="$HOME/devops/backups"
FECHA="$(date +%Y%m%d_%H%M%S)"
NOMBRE_BACKUP="scripts_backup_${FECHA}.tar.gz"

echo "[$(date)] Iniciando backup..."
tar -czf "${DESTINO}/${NOMBRE_BACKUP}" "${ORIGEN}"

if [ $? -eq 0 ]; then
  echo "[$(date)] Backup exitoso: ${NOMBRE_BACKUP}"
  echo "[$(date)] ${NOMBRE_BACKUP}" >> "$HOME/devops/logs/backups.log"
else
  echo "[$(date)] ERROR en el backup" >&2
  exit 1
fi
