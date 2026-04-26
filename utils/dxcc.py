from config import CTY_FILE


def load_cty() -> tuple[dict, dict]:
    prefixes: dict[str, str] = {}
    exact_calls: dict[str, str] = {}
    current_country: str | None = None

    with open(CTY_FILE, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if ":" in line:
                current_country = line.split(":")[0].strip()
                continue

            if not current_country:
                continue

            line = line.replace(";", "")
            for item in line.split(","):
                item = item.strip().upper()
                if not item:
                    continue

                is_exact = item.startswith("=")
                item = item.replace("=", "")
                item = item.split("(")[0].split("[")[0].strip()

                if not item:
                    continue

                if is_exact:
                    exact_calls[item] = current_country
                else:
                    prefixes[item] = current_country

    # Ordenar por longitud descendente para match greedy
    prefixes = dict(sorted(prefixes.items(), key=lambda x: -len(x[0])))
    return prefixes, exact_calls


def get_country(call: str, prefixes: dict, exact_calls: dict) -> str:
    call = call.upper()

    if call in exact_calls:
        return exact_calls[call]

    for prefix in prefixes:
        if call.startswith(prefix):
            return prefixes[prefix]

    return "UNKNOWN"


# Cargado una sola vez al importar el módulo
PREFIXES, EXACT_CALLS = load_cty()
