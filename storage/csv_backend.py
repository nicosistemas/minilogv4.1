import csv
import os

from config import USERS_DIR
from storage.base import BaseStorage


class CSVStorage(BaseStorage):
    """
    Backend CSV: un archivo contacts.csv por usuario en data/users/<callsign>/
    """

    def _user_dir(self, user_id: str) -> str:
        path = os.path.join(USERS_DIR, user_id.upper())
        os.makedirs(path, exist_ok=True)
        return path

    def _contacts_path(self, user_id: str) -> str:
        return os.path.join(self._user_dir(user_id), "contacts.csv")

    def load_contacts(self, user_id: str) -> list[list]:
        path = self._contacts_path(user_id)
        if not os.path.exists(path):
            return []
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.reader(f))

    def save_contacts(self, user_id: str, contacts: list[list]) -> None:
        path = self._contacts_path(user_id)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(contacts)

    def append_contact(self, user_id: str, contact: list) -> None:
        contacts = self.load_contacts(user_id)
        contacts.append(contact)
        self.save_contacts(user_id, contacts)

    def delete_contact(self, user_id: str, index: int) -> None:
        contacts = self.load_contacts(user_id)
        if index < 0 or index >= len(contacts):
            raise IndexError(f"Índice {index} fuera de rango")
        contacts.pop(index)
        self.save_contacts(user_id, contacts)

    def update_contact(self, user_id: str, index: int, contact: list) -> None:
        contacts = self.load_contacts(user_id)
        if index < 0 or index >= len(contacts):
            raise IndexError(f"Índice {index} fuera de rango")
        contacts[index] = contact
        self.save_contacts(user_id, contacts)
