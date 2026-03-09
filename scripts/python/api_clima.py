import requests
import socket
from datetime import datetime

old_getaddrinfo = socket.getaddrinfo
def ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
  return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = ipv4_only

# Open-Meteo: API de clima open source, sin API key
# Coordenadas de Yumbo, Valle del Cauca
URL = "https://api.open-meteo.com/v1/forecast?latitude=3.6&longitude=-76.5&current_weather=true"

try:
  response = requests.get(URL, timeout=10)
  response.raise_for_status()

  datos = response.json()
  clima = datos["current_weather"]

  print(f"🌤  Clima en Yumbo — {datetime.now().strftime('%H:%M')}")
  print(f"🌡  Temperatura: {clima['temperature']}°C")
  print(f"💨 Viento:      {clima['windspeed']} km/h")
  print(f"🕐 Hora dato:   {clima['time']}")

except requests.exceptions.RequestException as e:
  print(f"Error al llamar la API: {e}")
