from datetime import date


def days_until_deadline(deadline: date | None) -> int | None:
    if not deadline:
        return None
    return (deadline - date.today()).days


def deadline_badge(deadline: date | None) -> dict | None:
    days = days_until_deadline(deadline)
    if days is None:
        return None
    if days < 0:
        return {"text": "마감", "class": "badge-closed"}
    if days <= 7:
        return {"text": f"D-{days}", "class": "badge-urgent"}
    if days <= 30:
        return {"text": f"D-{days}", "class": "badge-soon"}
    return {"text": f"D-{days}", "class": "badge-normal"}
