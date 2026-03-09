import json, os, subprocess
from datetime import datetime

HOME   = os.path.expanduser("~")
CONFIG = f"{HOME}/devops/configs/servidores.json"
LOG    = f"{HOME}/devops/logs/monitor_completo.log"

def log(msg):
  ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  linea = f"[{ts}] {msg}"
  print(linea)
  with open(LOG, "a") as f:
    f.write(linea + "\n")

def ping(ip):
  r = subprocess.run(
    ["ping", "-c", "1", "-W", "2", ip],
    capture_output=True
  )
  return r.returncode == 0

with open(CONFIG) as f:
  config = json.load(f)

activos = 0
caidos  = 0

log(f"=== Monitor: {config['proyecto']} ===")

for srv in config["servidores"]:
  ip     = srv["ip"]
  nombre = srv["nombre"]
  if ping(ip):
    log(f"✓ ACTIVO   {nombre} ({ip})")
    activos += 1
  else:
    log(f"✗ CAIDO    {nombre} ({ip})")
    caidos += 1

log(f"--- Resumen: {activos} activos, {caidos} caídos ---")
# v1.1 — agregado resumen final
