BANDS = [
    (1.8,    2.0,    "160m"),
    (3.5,    4.0,    "80m"),
    (5.0,    5.5,    "60m"),
    (7.0,    7.3,    "40m"),
    (10.1,   10.15,  "30m"),
    (14.0,   14.35,  "20m"),
    (18.068, 18.168, "17m"),
    (21.0,   21.45,  "15m"),
    (24.89,  24.99,  "12m"),
    (28.0,   29.7,   "10m"),
    (50.0,   54.0,   "6m"),
    (144.0,  148.0,  "2m"),
    (430.0,  450.0,  "70cm"),
]


def get_band(frequency: str | float) -> str:
    try:
        freq = float(frequency)
    except (ValueError, TypeError):
        return "UNKNOWN"

    for low, high, band in BANDS:
        if low <= freq < high:
            return band

    return "UNKNOWN"
