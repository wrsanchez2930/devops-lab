from crewai import Task
from agentes import analista, redactor, coordinador

DATOS_INFRA = """
Network Inventory Report:
- Total devices: 9, Active: 9, Inactive: 0
- Sites: CPD Yumbo, CPD Ibague, Jamundi, Brisas
- Firewalls: FW-YUMBO-01 (10.10.0.1), FW-IBAGUE-01 (10.30.0.1) - Fortinet
- Core: CORE-YUMBO-MX480-01 (10.10.0.2), CORE-IBAGUE-NE40-01 (10.30.0.2) - Juniper
- Transport: AGG-YUMBO-NE40-01, MPLS-BRI-01, MPLS-JAM-01 - Huawei
- OLT: OLT-BRI-01 (10.40.0.1), OLT-JAM-01 (10.20.0.1) - Huawei
"""

tarea_analisis = Task(
  description=f"""Analyze the following network infrastructure data and identify:
1. Total device count and status
2. Devices by role and manufacturer
3. Any potential issues or observations

Data: {DATOS_INFRA}""",
  expected_output="Structured analysis with device counts, roles, manufacturers, and observations",
  agent=analista
)

tarea_reporte = Task(
  description="""Using the analysis from the previous task, write a concise infrastructure report with:
- Executive summary (2 sentences)
- Device inventory by role
- Overall status""",
  expected_output="Professional infrastructure report in markdown format",
  agent=redactor
)

tarea_coordinacion = Task(
  description="""Review the infrastructure report and provide:
1. Overall status: GREEN, YELLOW, or RED
2. Top 3 recommended actions for the NOC team
3. Next scheduled review""",
  expected_output="NOC action plan with status, recommendations and next review",
  agent=coordinador
)

print("✓ 3 tareas definidas")
