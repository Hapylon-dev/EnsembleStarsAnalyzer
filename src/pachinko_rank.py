"""OVERALL PACHINKO rank thresholds and palette (3.3.0-dev fixed specification)."""
RANK_THRESHOLDS = (
    (60000, "SSS+"), (50400, "SSS"), (44700, "SS+"), (40500, "SS"),
    (36900, "S+"), (33300, "S"), (29700, "AAA+"), (26400, "AAA"),
    (23400, "AA+"), (20700, "AA"), (18300, "A+"), (15900, "A"),
    (14100, "BBB"), (12300, "BB"), (9900, "B"), (7800, "CCC"),
    (5400, "CC"), (3300, "C"), (1800, "D"), (1500, "E"), (300, "F"),
)
RANK_COLORS = {
    "SSS+": "rainbow", "SSS": "rainbow",
    "SS+": "gold", "SS": "gold", "S+": "gold", "S": "gold",
    "AAA+": "red", "AAA": "red", "AA+": "red", "AA": "red", "A+": "red", "A": "red",
    "BBB": "blue", "BB": "blue", "B": "blue",
    "CCC": "green", "CC": "green", "C": "green",
    "D": "pink", "E": "purple", "F": "gray",
}


def get_pachinko_rank(total_notes: int) -> str:
    value = int(total_notes)
    for minimum, rank in RANK_THRESHOLDS:
        if value >= minimum:
            return rank
    return "F"
