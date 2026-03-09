import os, socket, subprocess
from datetime import datetime
from fastapi import FastAPI

app = FastAPI(
  title="DevOps Infra API",
  description="API de automatización de infraestructura",
  version="1.0.0"
)

@app.get("/", tags=["health"])
def health_check():
  return {
    "status": "ok",
    "timestamp": datetime.now().isoformat(),
    "version": "1.0.0"
  }

@app.get("/info", tags=["sistema"])
def info_servidor():
  return {
    "hostname": socket.gethostname(),
    "uptime": subprocess.getoutput("uptime -p"),
    "python": subprocess.getoutput("python3 --version")
  }

import requests as req

NETBOX_URL = "http://127.0.0.1:8000"
NETBOX_TOKEN = "pZqCZA51eqGybDJH9DfjyaX8H03N3ssWJsheAP7e"
HEADERS = {"Authorization": f"Token {NETBOX_TOKEN}"}

@app.get("/devices", tags=["netbox"])
def listar_dispositivos(rol: str = None, sitio: str = None):
  url = f"{NETBOX_URL}/api/dcim/devices/?limit=100&format=json"
  data = req.get(url, headers=HEADERS, timeout=30).json()
  dispositivos = [{
    "id": d["id"],
    "nombre": d["name"],
    "estado": d["status"]["value"],
    "ip": d["primary_ip"]["address"] if d.get("primary_ip") else None,
    "sitio": d["site"]["name"] if d.get("site") else None,
    "rol": d["role"]["name"] if d.get("role") else None
  } for d in data.get("results", [])]
  if rol: dispositivos = [d for d in dispositivos if d["rol"] == rol]
  if sitio: dispositivos = [d for d in dispositivos if d["sitio"] == sitio]
  return {"total": len(dispositivos), "dispositivos": dispositivos}

import requests as req

NETBOX_URL = "http://127.0.0.1:8000"
NETBOX_TOKEN = "pZqCZA51eqGybDJH9DfjyaX8H03N3ssWJsheAP7e"
HEADERS = {"Authorization": f"Token {NETBOX_TOKEN}"}

@app.get("/devices", tags=["netbox"])
def listar_dispositivos(rol: str = None, sitio: str = None):
  url = f"{NETBOX_URL}/api/dcim/devices/?limit=100&format=json"
  data = req.get(url, headers=HEADERS, timeout=30).json()
  dispositivos = [{
    "id": d["id"],
    "nombre": d["name"],
    "estado": d["status"]["value"],
    "ip": d["primary_ip"]["address"] if d.get("primary_ip") else None,
    "sitio": d["site"]["name"] if d.get("site") else None,
    "rol": d["role"]["name"] if d.get("role") else None
  } for d in data.get("results", [])]
  if rol: dispositivos = [d for d in dispositivos if d["rol"] == rol]
  if sitio: dispositivos = [d for d in dispositivos if d["sitio"] == sitio]
  return {"total": len(dispositivos), "dispositivos": dispositivos}

import json as json_lib
from pathlib import Path

SCRIPT = "/home/vboxuser/devops/scripts/python/netbox_reporte.py"
REPORTE = "/home/vboxuser/devops/proyectos/n8n/files/netbox-reporte.json"

@app.post("/monitor/run", tags=["monitor"])
def ejecutar_monitor():
  resultado = subprocess.run(
    ["python3", SCRIPT],
    capture_output=True, text=True, timeout=30
  )
  if resultado.returncode != 0:
    return {"ok": False, "error": resultado.stderr}
  return {"ok": True, "output": resultado.stdout.strip()}

@app.get("/report", tags=["monitor"])
def obtener_reporte():
  if not Path(REPORTE).exists():
    return {"error": "Reporte no generado aún. POST /monitor/run primero"}
  with open(REPORTE) as f:
    return json_lib.load(f)

from pydantic import BaseModel
from typing import Optional

class Alerta(BaseModel):
  dispositivo: str
  severidad: str
  mensaje: str
  ip: Optional[str] = None

alertas_recibidas = []

@app.post("/webhook/alerta", tags=["webhook"])
def recibir_alerta(alerta: Alerta):
  entrada = {**alerta.dict(), "timestamp": datetime.now().isoformat()}
  alertas_recibidas.append(entrada)
  return {"recibido": True, "total_alertas": len(alertas_recibidas)}

@app.get("/webhook/alertas", tags=["webhook"])
def ver_alertas():
  return {"total": len(alertas_recibidas), "alertas": alertas_recibidas}
