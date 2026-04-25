from config import STORAGE_BACKEND
from storage.base import BaseStorage


def get_storage() -> BaseStorage:
    """
    Factory: retorna el backend configurado en STORAGE_BACKEND.
    Para agregar SQLite: implementar SQLiteStorage y agregar el caso acá.
    """
    if STORAGE_BACKEND == "csv":
        from storage.csv_backend import CSVStorage
        return CSVStorage()

    # Ejemplo futuro:
    # if STORAGE_BACKEND == "sqlite":
    #     from storage.sqlite_backend import SQLiteStorage
    #     return SQLiteStorage()

    raise ValueError(f"Backend de storage desconocido: {STORAGE_BACKEND}")


storage = get_storage()
