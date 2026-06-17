import subprocess
from datetime import datetime

PERSONAS={"arska":"rentoa","consultant":"tiukka","coach":"motivaatio","zen":"rauhallinen"}

def run(prompt):
    try:
        r=subprocess.run(["ollama","run","mistral"],input=prompt.encode(),stdout=subprocess.PIPE)
        return r.stdout.decode()
    except:
        return prompt


def smart_decision(data,persona):
    return run(f"Persoona:{PERSONAS.get(persona)} Data:{data} Anna suositus")
