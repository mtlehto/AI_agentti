import subprocess

PERSONAS={"arska":"rentoa","consultant":"tiukka","coach":"motivaatio","zen":"rauhallinen"}

def run(prompt):
    try:
        r = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return r.stdout.strip() or "En saanut suositusta juuri nyt."
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return "En saanut suositusta juuri nyt."


def smart_decision(data,persona):
    return run(f"Persoona:{PERSONAS.get(persona, 'rentoa')} Data:{data} Anna suositus")
