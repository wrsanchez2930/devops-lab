import requests, json, os, socket
from datetime import datetime

# Forzar IPv4
old = socket.getaddrinfo
def ipv4(host, port, family=0, type=0, proto=0, flags=0):
  return old(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = ipv4

TOKEN = "pZqCZA51eqGybDJH9DfjyaX8H03N3ssWJsheAP7e"
URL   = "http://127.0.0.1:8000/api/dcim/devices/?limit=100&format=json"
LOG   = os.path.expanduser("~/devops/proyectos/n8n/files/netbox-reporte.json")

headers = {"Authorization": f"Token {TOKEN}"}
data = requests.get(URL, headers=headers, timeout=10).json()

dispositivos = [{
  "nombre": d["name"],
  "estado": d["status"]["value"],
  "ip": d["primary_ip"]["address"] if d.get("primary_ip") else "sin IP",
  "sitio": d["site"]["name"] if d.get("site") else "sin sitio",
  "rol": d["role"]["name"] if d.get("role") else "sin rol",
  "fabricante": d["device_type"]["manufacturer"]["name"] if d.get("device_type") else "?"
} for d in data.get("results", [])]

reporte = {
  "generado": datetime.now().isoformat(),
  "total": len(dispositivos),
  "activos": sum(1 for d in dispositivos if d["estado"] == "active"),
  "inactivos": sum(1 for d in dispositivos if d["estado"] != "active"),
  "dispositivos": dispositivos
}

with open(LOG, "w") as f:
  json.dump(reporte, f, indent=2, ensure_ascii=False)

print(f"Reporte generado: {reporte['total']} dispositivos, {reporte['activos']} activos")
