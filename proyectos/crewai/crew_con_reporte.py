import sys, os
sys.path.insert(0, '/home/vboxuser/devops/proyectos/crewai')
os.environ["OTEL_SDK_DISABLED"] = "true"
from datetime import datetime
from crewai import Crew, Process
from agentes import analista, redactor, coordinador
from tareas import tarea_analisis, tarea_reporte, tarea_coordinacion

crew = Crew(
  agents=[analista, redactor, coordinador],
  tasks=[tarea_analisis, tarea_reporte, tarea_coordinacion],
  process=Process.sequential,
  verbose=False
)

print("🚀 Ejecutando auditoría...\n")
resultado = crew.kickoff()

ts = datetime.now().strftime("%Y%m%d_%H%M")
archivo = f"/home/vboxuser/devops/logs/auditoria_{ts}.md"
with open(archivo, "w") as f:
  f.write(f"# Auditoría de Infraestructura\n")
  f.write(f"**Fecha:** {datetime.now().isoformat()}\n\n")
  f.write(str(resultado))

print(f"✅ Reporte guardado: {archivo}")
