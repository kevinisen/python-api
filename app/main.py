from fastapi import FastAPI, Query
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import TicketCreate, TicketResponse, TicketUpdate, Status, Priority
from app.utils import load_tickets, save_tickets, sort_tickets
from app.script import count_tickets_by_status
from typing import List, Optional
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # ou [""] en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tickets", response_model=List[TicketResponse])
def get_tickets(
    status_order: Optional[List[Status]] = Query(None, description="Filtrer par status"),
    priority_order: Optional[str] = Query(None, pattern="^(asc|desc)$"),
    date_order: Optional[str] = Query(None, pattern="^(asc|desc)$")
):
    """
    Retourne la liste de tous les tickets trié selon les filtres.
    """
    tickets = load_tickets()
    return sort_tickets(tickets, status_order, date_order, priority_order)

@app.get("/tickets/stats")
def get_stats():
    return count_tickets_by_status()

@app.post("/tickets")
def create_ticket(ticket: TicketCreate, response_model=TicketResponse, status_code=201):
    print("🚀 POST /tickets appelé")
    """
    Crée un nouveau ticket.
    """
    tickets = load_tickets()

    # Générer un nouvel ID
    # Récupere toute la liste des tickets max(ticket["id"] for ticket in tickets) et prends son max et on rajoute 1
    # Ternaire Python => X if tickets else 1 (Si tickets existe je fais X sinon je else)
    new_id = max(ticket["id"] for ticket in tickets) + 1 if tickets else 1

    new_ticket = {
        "id": new_id,
        "createdAt": date.today().isoformat(),
        # ** unpacking d'un dic (copie chaque clé/valeur dans ce dictionnaire) équivalent a ... en JS
        # model_dump est une fonction pydantic et cela transforme un modele Python en dictionnaire.
        **ticket.model_dump(mode="json")
    }

    tickets.append(new_ticket)
    save_tickets(tickets)

    return new_ticket

@app.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, updates: TicketUpdate):
    tickets = load_tickets()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            # Recupere les data sous forme de de dict, exclude_unset=True retourne uniquement les champs envoyés
            update_data = updates.model_dump(exclude_unset=True)

            # Update du ticket choisi
            for key, value in update_data.items():
                ticket[key] = value

            save_tickets(tickets)
            return ticket

    raise HTTPException(status_code=404, detail="Ticket not found")

@app.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int):
    tickets = load_tickets()
    
    # Cherche le ticket
    ticket = next((t for t in tickets if t["id"] == ticket_id), None)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Supprime le ticket
    tickets.remove(ticket)
    
    save_tickets(tickets)
    
    # 204 = No Content
    return