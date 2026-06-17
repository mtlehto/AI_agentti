from fastapi import FastAPI
from agent.main import run_agent
app=FastAPI()
@app.get("/morning")
def morning(persona:str="arska"):
    return {"text":run_agent(persona)}
