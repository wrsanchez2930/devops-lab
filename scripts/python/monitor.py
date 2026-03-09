import subprocess
import os
from datetime import datetime

SERVIDORES = [
  "192.168.1.7",    # netbox-vm
  "8.8.8.8",        # Google DNS
  "192.168.1.99",   # IP inexistente (para ver falla)
]

LOG = f"{os.path.expanduser('~')}/devops/logs/monitor.log"

def ping(ip):
  r = subprocess.run(
    ["ping", "-c", "1", "-W", "2", ip],
    capture_output=True
  )
  return r.returncode == 0

def escribir_log(mensaje):
  ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  linea = f"[{ts}] {mensaje}"
  print(linea)
  with open(LOG, "a") as f:
    f.write(linea + "\n")

escribir_log("=== Inicio de monitoreo ===")
for ip in SERVIDORES:
  if ping(ip):
    escribir_log(f"✓ ACTIVO   {ip}")
  else:
    escribir_log(f"✗ INACTIVO {ip}")
