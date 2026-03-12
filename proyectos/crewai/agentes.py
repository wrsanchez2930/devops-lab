from crewai import Agent, LLM

llm = LLM(
  model="ollama/llama3.2:1b",
  base_url="http://127.0.0.1:11434"
)

analista = Agent(
  role="Network Infrastructure Analyst",
  goal="Collect and analyze network infrastructure data",
  backstory="""Expert network analyst for a Colombian ISP.
Infrastructure: 9 devices across 4 sites. Firewalls: Fortinet. Core: Juniper. Transport/OLT: Huawei.""",
  llm=llm,
  verbose=True
)

redactor = Agent(
  role="Technical Report Writer",
  goal="Write clear, structured technical reports from infrastructure data",
  backstory="Technical writer specialized in network operations reports.",
  llm=llm,
  verbose=True
)

coordinador = Agent(
  role="NOC Coordinator",
  goal="Review reports and prioritize actions for the network operations team",
  backstory="NOC coordinator with 10 years of experience.",
  llm=llm,
  verbose=True
)

print("✓ 3 agentes definidos:")
print(f"  - {analista.role}")
print(f"  - {redactor.role}")
print(f"  - {coordinador.role}")
