from pathlib import Path
import json
from app.models import Status
from typing import List

DATA_FILE = Path("tickets.json")

def load_tickets():
    """
    Charge les tickets depuis le fichier JSON.
    """
    # le with permet de génrer automatiquement une ressource quand le bloc with se termine il va le fermer automatiquement
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def save_tickets(tickets: list):
    """
    Sauvegarde les tickets dans le fichier JSON.
    """
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)

def sort_tickets(tickets, status_order: List[Status] | None = None, date_order: str | None = None, priority_order: str | None = None):
    """
    Trie les tickets selon la priorité et/ou la date.
    
    - priority_order : "asc" / "desc" ou None → tri par priorité si défini
    - date_order     : "asc" / "desc" ou None → tri par date si défini
    """

    PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}
    if status_order is not None:
        tickets = sort_by_status(tickets, status_order)

    if date_order is not None and priority_order is None:
        tickets = sort_by_date(tickets, date_order)

    if priority_order is not None:
        tickets = sort_by_priority(tickets, priority_order, date_order)

    return tickets

def sort_by_status(tickets, status_order):
    print([s.value for s in status_order])
    return [t for t in tickets if t["status"] in [s.value for s in status_order]]

def sort_by_date(tickets, date_order):
    reverse_order = date_order == "asc"
    return sorted(tickets, key=lambda t: t["createdAt"], reverse=reverse_order)

def sort_by_priority(tickets, priority_order, date_order):
    reverse_order = date_order == "asc" or date_order == None
    high = sorted([t for t in tickets if t["priority"] == "High"], key=lambda t: t["createdAt"], reverse=reverse_order)
    medium = sorted([t for t in tickets if t["priority"] == "Medium"], key=lambda t: t["createdAt"], reverse=reverse_order)
    low = sorted([t for t in tickets if t["priority"] == "Low"], key=lambda t: t["createdAt"], reverse=reverse_order)

    if priority_order == "asc":
        return high + medium + low
    else:
        return low + medium + high
