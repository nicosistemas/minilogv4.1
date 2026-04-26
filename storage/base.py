from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """
    Interfaz base para el backend de almacenamiento.
    Implementar esta clase para agregar nuevos backends (SQLite, PostgreSQL, etc.)
    """

    @abstractmethod
    def load_contacts(self, user_id: str) -> list[list]:
        """Retorna lista de contactos del usuario."""
        ...

    @abstractmethod
    def save_contacts(self, user_id: str, contacts: list[list]) -> None:
        """Guarda la lista completa de contactos del usuario."""
        ...

    @abstractmethod
    def append_contact(self, user_id: str, contact: list) -> None:
        """Agrega un contacto al log del usuario."""
        ...

    @abstractmethod
    def delete_contact(self, user_id: str, index: int) -> None:
        """Elimina un contacto por índice."""
        ...

    @abstractmethod
    def update_contact(self, user_id: str, index: int, contact: list) -> None:
        """Actualiza un contacto por índice."""
        ...
