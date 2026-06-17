from agent.graph import get_token
from agent.email import get_emails
from agent.calendar import get_calendar
from agent.tasks import get_tasks
from agent.route import get_public_time,get_car_time
from agent.traffic import get_transit_delay,get_traffic_level
from agent.ai import smart_decision
from agent.tts import speak
from agent.teams import send


def build_brief(persona="arska"):
    t=get_token()
    e=get_emails(t)
    c=get_calendar(t)
    tasks=get_tasks(t)

    pub=get_public_time()
    car=get_car_time()
    delay=get_transit_delay()
    traffic=get_traffic_level(car)

    data=f"emails:{e} calendar:{c} tasks:{tasks} public:{pub} car:{car} delay:{delay} traffic:{traffic}"

    decision=smart_decision(data,persona)

    return {
        "persona": persona,
        "emails": e,
        "calendar": c,
        "tasks": tasks,
        "public_time": pub,
        "car_time": car,
        "transit_delay": delay,
        "traffic_level": traffic,
        "text": decision,
    }


def run_agent(persona="arska", deliver=True):
    brief = build_brief(persona)
    decision = brief["text"]

    if deliver:
        speak(decision)
        send(get_token(), decision)

    return brief
