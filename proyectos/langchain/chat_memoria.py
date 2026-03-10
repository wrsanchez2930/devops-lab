from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = OllamaLLM(model="tinyllama", base_url="http://127.0.0.1:11434")

# Historial manual (memoria simple)
historial = []

def chat(mensaje):
  historial.append(HumanMessage(content=mensaje))
  prompt = "\n".join([
    f"Human: {m.content}" if isinstance(m, HumanMessage) else f"AI: {m.content}"
    for m in historial
  ])
  respuesta = llm.invoke(prompt)
  historial.append(AIMessage(content=respuesta))
  return respuesta

# Turno 1
r1 = chat("My network has 2 Fortinet firewalls. Remember this.")
print(f"Turn 1: {r1[:200]}")

# Turno 2 — debe recordar
r2 = chat("What brand are the firewalls I mentioned?")
print(f"\nTurn 2: {r2[:200]}")

print(f"\n=== Historial: {len(historial)} mensajes ===")
