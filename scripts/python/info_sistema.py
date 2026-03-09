import os
import subprocess
from datetime import datetime

ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
usuario = os.getenv("USER")
home = os.path.expanduser("~")

hostname = subprocess.run(
  ["hostname"], capture_output=True, text=True
).stdout.strip()

carpetas = os.listdir(f"{home}/devops")

print("=" * 40)
print("  REPORTE DE SISTEMA")
print("=" * 40)
print(f"Fecha:    {ahora}")
print(f"Servidor: {hostname}")
print(f"Usuario:  {usuario}")
print(f"Home:     {home}")
print(f"Devops:   {', '.join(carpetas)}")
print("=" * 40)
