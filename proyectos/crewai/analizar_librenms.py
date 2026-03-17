import sys, os, json
sys.path.insert(0, '/home/vboxuser/devops/proyectos/crewai')
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent, Task, Crew, Process, LLM
from datetime import datetime

with open('/home/vboxuser/devops/logs/reporte_mpls_completo.json') as f:
    datos = json.load(f)

resumen = datos['resumen']

def parse_bps(s):
    try:
        s = s.strip()
        if 'Gbps' in s: return float(s.replace(' Gbps','')) * 1e9
        if 'Mbps' in s: return float(s.replace(' Mbps','')) * 1e6
        if 'Kbps' in s: return float(s.replace(' Kbps','')) * 1e3
        return float(s.replace(' bps',''))
    except: return 0

top5 = sorted(datos['dispositivos'], key=lambda x: parse_bps(x['trafico_in']), reverse=True)[:5]

contexto = f"""
Red MPLS real - {datos['timestamp']}
Total: {resumen['total_dispositivos']} dispositivos | UP: {resumen['up']} | DOWN: {resumen['down']}
Trafico IN: {resumen['trafico_total_in']} | OUT: {resumen['trafico_total_out']}
Errores: {resumen['dispositivos_con_errores']}

Top 5 por trafico:
"""
for d in top5:
    contexto += f"- {d['nombre']}: IN={d['trafico_in']} OUT={d['trafico_out']} ({d['puertos_up']} puertos)\n"

primer = top5[0]
contexto += f"\nInterfaces de {primer['nombre']}:\n"
top_ifaces = sorted(primer['interfaces'], key=lambda x: x['in_bps'], reverse=True)[:5]
for i in top_ifaces:
    contexto += f"  {i['nombre']} {i['velocidad']}: IN={i['in_human']} OUT={i['out_human']} {i['alias'][:40]}\n"

llm = LLM(model="ollama/llama3.2:1b", base_url="http://127.0.0.1:11434")

analista = Agent(
    role="Network Traffic Analyst",
    goal="Analyze real MPLS network traffic and identify risks",
    backstory="Expert analyst for a Colombian ISP with 1.6 Tbps MPLS backbone.",
    llm=llm, verbose=False
)

coordinador = Agent(
    role="NOC Coordinator",
    goal="Provide actionable NOC recommendations based on network data",
    backstory="NOC coordinator responsible for MPLS backbone operations.",
    llm=llm, verbose=False
)

tarea_analisis = Task(
    description=f"Analyze this real MPLS network data and identify health status, traffic patterns and risks:\n{contexto}",
    expected_output="Network health assessment with traffic analysis and risks",
    agent=analista
)

tarea_recomendaciones = Task(
    description="Based on the analysis give: 1) Status GREEN/YELLOW/RED 2) Top 3 NOC actions 3) Capacity observations",
    expected_output="NOC action plan with status and top 3 recommendations",
    agent=coordinador
)

crew = Crew(
    agents=[analista, coordinador],
    tasks=[tarea_analisis, tarea_recomendaciones],
    process=Process.sequential,
    verbose=False
)

print("🚀 Analizando red MPLS con CrewAI...\n")
resultado = crew.kickoff()

ts = datetime.now().strftime("%Y%m%d_%H%M")
archivo = f"/home/vboxuser/devops/logs/analisis_mpls_{ts}.md"
with open(archivo, "w") as f:
    f.write(f"# Análisis MPLS — {datetime.now().isoformat()}\n\n")
    f.write(f"## Contexto\n{contexto}\n\n## Análisis\n{str(resultado)}")

print("="*60)
print(str(resultado)[:800])
print(f"\n✅ Guardado: {archivo}")
