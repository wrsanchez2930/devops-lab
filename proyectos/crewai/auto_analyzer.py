import sys, os, json
sys.path.insert(0, '/home/vboxuser/devops/proyectos/crewai')
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent, Task, Crew, Process, LLM
from datetime import datetime
from pathlib import Path

REPORTE = "/home/vboxuser/devops/logs/hub_latest.json"
LOG_DIR = Path("/home/vboxuser/devops/logs")

with open(REPORTE) as f:
    data = json.load(f)

lnms    = data["librenms"]
alertas = lnms["alertas"]

down_names  = [d['nombre'] for d in lnms.get("dispositivos_down",[])[:5]]
top_trafico = []
for d in lnms.get("trafico_mpls",[])[:3]:
    if d.get("top_interfaces"):
        t = d["top_interfaces"][0]
        top_trafico.append(f"{d['nombre']}:{t['in_gbps']}G")

contexto = f"""Network: {lnms['total']} devices UP:{lnms['up']} DOWN:{lnms['down']}
Alerts critical:{alertas['criticas']} warning:{alertas['warnings']}
DOWN: {', '.join(down_names) if down_names else 'none'}
Traffic: {', '.join(top_trafico)}
Subnets: {data['phpipam']['total_subredes']}"""

llm = LLM(
    model="ollama/llama3.2:1b",
    base_url="http://127.0.0.1:11434",
    timeout=120
)

coordinador = Agent(
    role="NOC Coordinator",
    goal="Write a short NOC report",
    backstory="You write short NOC reports. Always complete your answer.",
    llm=llm, verbose=False
)

tarea = Task(
    description=f"""Write a NOC report using EXACTLY this format, filling in the blanks:

STATUS: [GREEN or YELLOW or RED]
REASON: [one sentence]
ACTION1: [specific task for NOC team]
ACTION2: [specific task for NOC team]
ACTION3: [specific task for NOC team]

Network data to analyze:
{contexto}""",
    expected_output="STATUS, REASON, ACTION1, ACTION2, ACTION3 — exactly 5 lines",
    agent=coordinador
)

crew = Crew(
    agents=[coordinador],
    tasks=[tarea],
    process=Process.sequential,
    verbose=False
)

print(f"Analizando {data['timestamp'][:16]}...")
resultado = crew.kickoff()

ts_file  = datetime.now().strftime("%Y%m%d_%H%M")
archivo  = LOG_DIR / f"analisis_{ts_file}.md"
contenido = f"# NOC Report — {datetime.now().isoformat()}\n\n## Snapshot\n{contexto}\n\n## Analysis\n{str(resultado)}\n"

with open(archivo, "w") as f:
    f.write(contenido)
with open(LOG_DIR / "analisis_latest.md", "w") as f:
    f.write(contenido)

print("\n" + "="*50)
print(str(resultado))
print(f"\n✅ {archivo}")
