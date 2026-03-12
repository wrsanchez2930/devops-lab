import sys, os
sys.path.insert(0, '/home/vboxuser/devops/proyectos/crewai')
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Crew, Process
from agentes import analista, redactor, coordinador
from tareas import tarea_analisis, tarea_reporte, tarea_coordinacion

crew = Crew(
  agents=[analista, redactor, coordinador],
  tasks=[tarea_analisis, tarea_reporte, tarea_coordinacion],
  process=Process.sequential,
  verbose=True
)

print("🚀 Iniciando auditoría de infraestructura...\n")
resultado = crew.kickoff()

print("\n" + "="*50)
print("✅ AUDITORÍA COMPLETADA")
print("="*50)
print(resultado)
