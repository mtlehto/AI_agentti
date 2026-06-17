from fastapi import FastAPI
from agent.main import build_brief, run_agent
app=FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/brief")
def brief(persona:str="arska"):
    return build_brief(persona)

@app.get("/morning")
def morning(persona:str="arska"):
    return run_agent(persona)
