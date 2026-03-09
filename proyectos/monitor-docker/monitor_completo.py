import json, os, subprocess
from datetime import datetime

# Buscar config en la misma carpeta del script (funciona en Docker y en la VM)
BASE   = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE, "servidores.json")
LOG    = os.path.join(BASE, "monitor.log")

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
  if ping(srv["ip"]):
    log(f"✓ ACTIVO   {srv['nombre']} ({srv['ip']})")
    activos += 1
  else:
    log(f"✗ CAIDO    {srv['nombre']} ({srv['ip']})")
    caidos += 1

log(f"--- Resumen: {activos} activos, {caidos} caídos ---")
