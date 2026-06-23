from agent.graph import get_token
from agent.email import get_emails
from agent.calendar import get_calendar
from agent.tasks import get_tasks
from agent.route import get_public_time,get_car_time
from agent.traffic import get_transit_delay,get_traffic_level
from agent.ai import smart_decision
from agent.tts import speak
from agent.teams import send
from agent.push import send_push


def build_brief(persona="arska", token=None):
    if token is None:
        token = get_token()

    emails = get_emails(token) if token else []
    calendar = get_calendar(token) if token else []
    tasks = get_tasks(token) if token else []

    pub = get_public_time()
    car = get_car_time()
    delay = get_transit_delay()
    traffic = get_traffic_level(car)

    data = (
        f"emails:{' | '.join(emails)} "
        f"calendar:{' | '.join(calendar)} "
        f"tasks:{' | '.join(tasks)} "
        f"public:{pub} car:{car} delay:{delay} traffic:{traffic}"
    )

    decision = smart_decision(data, persona)

    brief = {
        "persona": persona,
        "emails": emails,
        "calendar": calendar,
        "tasks": tasks,
        "public_time": pub,
        "car_time": car,
        "transit_delay": delay,
        "traffic_level": traffic,
        "text": decision,
    }

    if not token:
        brief["warning"] = "Graph token unavailable; email, calendar and task data may be missing."

    return brief


def run_agent(persona="arska", deliver=True):
    token = get_token()
    brief = build_brief(persona, token)
    decision = brief["text"]

    if deliver:
        speak(decision)
        if token:
            send(token, decision)
        else:
            print("Warning: Teams delivery skipped because Graph token is unavailable.")
        send_push(decision)

    return brief
