import requests, json

def preguntar(prompt):
  r = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={"model": "tinyllama", "prompt": prompt, "stream": False},
    timeout=300
  )
  return r.json()["response"]

with open("/home/vboxuser/devops/proyectos/n8n/files/netbox-reporte.json") as f:
  reporte = json.load(f)

inventario = "\n".join([
  f"- {d['nombre']} | {d['rol']} | {d['sitio']} | {d['ip']}"
  for d in reporte["dispositivos"]
])

prompt = f"""You are a network engineer. Given this inventory:
{inventario}

Answer briefly:
1. How many sites?
2. Which devices are firewalls and what brand?
3. One security recommendation."""

print("Analizando inventario con IA...\n")
print(preguntar(prompt))
