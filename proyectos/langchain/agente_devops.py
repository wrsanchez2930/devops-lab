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

agente = create_agent(
  model=llm,
  tools=[listar_dispositivos, ejecutar_monitor, obtener_reporte],
  system_prompt="""You are NetOps-AI, network operations assistant for a Colombian ISP.
Infrastructure: 9 devices across 4 sites. Firewalls: Fortinet. Core: Juniper. Transport/OLT: Huawei.
Always use obtener_reporte for inventory summaries and listar_dispositivos for device lists."""
)

print("=== NetOps-AI Agent ===")
r = agente.invoke({"messages": [
  {"role": "user", "content": "Run the monitor and give me a summary of the infrastructure status."}
]})
print(f"Respuesta: {r['messages'][-1].content}")
