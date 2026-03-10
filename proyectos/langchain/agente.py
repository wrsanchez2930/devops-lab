import sys
sys.path.insert(0, '/home/vboxuser/devops/proyectos/langchain')

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from tools_infra import listar_dispositivos, ejecutar_monitor, obtener_reporte

llm = ChatOllama(
  model="llama3.2:1b",
  base_url="http://127.0.0.1:11434",
  temperature=0
)

tools = [listar_dispositivos, ejecutar_monitor, obtener_reporte]

agente = create_agent(
  model=llm,
  tools=tools,
  system_prompt="""You are NetOps-AI. Use tools to answer questions.
- Use obtener_reporte to get inventory summary (total, active, inactive counts)
- Use listar_dispositivos with empty string "" to list all devices
- Use listar_dispositivos with "Firewall" to filter firewalls only"""
)

print("=== Test 1: Reporte general ===")
r1 = agente.invoke({"messages": [{"role": "user", "content": "Use obtener_reporte tool and tell me the total devices and how many are active."}]})
print(f"Respuesta: {r1['messages'][-1].content}")

print("\n=== Test 2: Firewalls ===")
r2 = agente.invoke({"messages": [{"role": "user", "content": "Use listar_dispositivos with input Firewall and list the firewall devices."}]})
print(f"Respuesta: {r2['messages'][-1].content}")
