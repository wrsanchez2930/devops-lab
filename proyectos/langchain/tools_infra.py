import requests, json
from langchain.tools import tool

API = "http://127.0.0.1:8080"

@tool
def listar_dispositivos(rol: str = "") -> str:
  """Lista dispositivos de red. Puedes filtrar por rol: Firewall, Core, Transporte, OLT"""
  url = f"{API}/devices"
  if rol: url += f"?rol={rol}"
  data = requests.get(url, timeout=10).json()
  return json.dumps(data, ensure_ascii=False)

@tool
def ejecutar_monitor(dummy: str = "") -> str:
  """Ejecuta el monitor de Netbox y devuelve el resultado"""
  r = requests.post(f"{API}/monitor/run", timeout=60)
  return r.json().get("output", "error")

@tool
def obtener_reporte(dummy: str = "") -> str:
  """Obtiene el último reporte de inventario generado"""
  data = requests.get(f"{API}/report", timeout=10).json()
  return f"Total: {data.get('total',0)}, Activos: {data.get('activos',0)}, Inactivos: {data.get('inactivos',0)}"

if __name__ == "__main__":
  print("=== Test listar_dispositivos ===")
  print(listar_dispositivos.invoke("Firewall"))
  print("\n=== Test obtener_reporte ===")
  print(obtener_reporte.invoke(""))
