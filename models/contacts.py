from datetime import datetime, timezone

from storage import storage


def load_contacts(user_id: str) -> list[list]:
    return storage.load_contacts(user_id)


def append_contact(user_id: str, callsign: str, mode: str,
                   frequency: str, notes: str) -> None:
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    contact = [date, callsign.upper(), mode, frequency, notes, user_id.upper()]
    storage.append_contact(user_id, contact)


def delete_contact(user_id: str, index: int) -> None:
    storage.delete_contact(user_id, index)


def update_contact(user_id: str, index: int, callsign: str,
                   mode: str, frequency: str, notes: str) -> None:
    contacts = load_contacts(user_id)
    if index < 0 or index >= len(contacts):
        raise IndexError("Contacto no encontrado")
    original_date = contacts[index][0]
    updated = [original_date, callsign.upper(), mode, frequency, notes, user_id.upper()]
    storage.update_contact(user_id, index, updated)
