import json
import os

CONFIG_PATH = f"{os.path.expanduser('~')}/devops/configs/servidores.json"

with open(CONFIG_PATH) as f:
  config = json.load(f)

print(f"Proyecto: {config['proyecto']}")
print(f"Intervalo: {config['intervalo_segundos']}s")
print(f"Servidores configurados:")

for srv in config["servidores"]:
  print(f"  → {srv['nombre']} ({srv['ip']}) — rol: {srv['rol']}")
