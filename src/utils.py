def clamp(value, minimum, maximum):

    return max(
        minimum,
        min(
            maximum,
            value
        )
    )


def calculate_precision(ratio):

    return round(
        ratio * 100,
        1
    )


def calculate_balance(fast, slow):

    total = fast + slow

    if total == 0:

        return 100.0

    diff = abs(
        fast - slow
    )

    score = (
        1 - diff / total
    ) * 100

    return round(
        score,
        1
    )


def calculate_overall(

    achievement,

    precision,

    balance

):

    score = (

        achievement * 0.4

        +

        precision * 0.3

        +

        balance * 0.3

    )

    return round(
        score,
        1
    )


def rank_precision(score):

    if score >= 90:
        return 6

    if score >= 80:
        return 5

    if score >= 70:
        return 4

    if score >= 60:
        return 3

    if score >= 50:
        return 2

    return 1


def rank_balance(score):

    if score >= 90:
        return 6

    if score >= 80:
        return 5

    if score >= 70:
        return 4

    if score >= 60:
        return 3

    if score >= 50:
        return 2

    return 1


def rank_overall(score):

    if score >= 95:
        return "SS"

    if score >= 85:
        return "S"

    if score >= 75:
        return "A"

    if score >= 65:
        return "B"

    if score >= 55:
        return "C"

    return "D"