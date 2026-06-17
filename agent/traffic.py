def get_transit_delay(): return 3

def get_traffic_level(car):
    if car>35: return "high"
    if car>30: return "medium"
    return "low"
