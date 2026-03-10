import requests, json

def preguntar(prompt, modelo="tinyllama"):
  r = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={"model": modelo, "prompt": prompt, "stream": False},
    timeout=300
  )
  return r.json()["response"]

# Test 1 — ya funciona, lo dejamos
print("=== BGP ===")
print(preguntar("Explain BGP routing in one paragraph."))

# Test 2 — prompt más corto para CPU
print("\n=== LOG ANALYSIS ===")
print(preguntar("This firewall log shows: DROP SRC=185.220.101.5 repeated 3 times. What does this mean in 2 sentences?"))
