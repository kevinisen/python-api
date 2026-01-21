from collections import defaultdict
from app.utils import load_tickets  # ou l'import que tu utilises

def count_tickets_by_status():
    tickets = load_tickets()

    counts = defaultdict(int)

    for ticket in tickets:
        counts[ticket["status"]] += 1

    return dict(counts)
