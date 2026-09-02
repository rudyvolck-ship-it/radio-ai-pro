from datetime import datetime

DAY_ORDER = ["ma", "di", "wo", "do", "vr", "za", "zo"]
DAY_ALIASES = {
    "ma": "ma",
    "mon": "ma",
    "monday": "ma",
    "maandag": "ma",
    "di": "di",
    "tue": "di",
    "tues": "di",
    "tuesday": "di",
    "dinsdag": "di",
    "wo": "wo",
    "wed": "wo",
    "wednesday": "wo",
    "woensdag": "wo",
    "do": "do",
    "thu": "do",
    "thur": "do",
    "thurs": "do",
    "thursday": "do",
    "donderdag": "do",
    "vr": "vr",
    "fri": "vr",
    "friday": "vr",
    "vrijdag": "vr",
    "za": "za",
    "sat": "za",
    "saturday": "za",
    "zaterdag": "za",
    "zo": "zo",
    "sun": "zo",
    "sunday": "zo",
    "zondag": "zo",
}
EN_WEEKDAY_TO_DAY = {
    "monday": "ma",
    "tuesday": "di",
    "wednesday": "wo",
    "thursday": "do",
    "friday": "vr",
    "saturday": "za",
    "sunday": "zo",
}


def normalize_day(day_value):
    if not day_value:
        return ""
    raw = str(day_value).strip().lower()
    return DAY_ALIASES.get(raw, "")


def normalize_days(days_value, legacy_day=None):
    if isinstance(days_value, str):
        days = [days_value]
    elif isinstance(days_value, list):
        days = days_value
    else:
        days = []

    if not days and legacy_day is not None:
        days = [legacy_day]

    normalized = []
    for day in days:
        normalized_day = normalize_day(day)
        if normalized_day and normalized_day not in normalized:
            normalized.append(normalized_day)
    return normalized


def time_to_minutes(time_value):
    try:
        hour_str, minute_str = str(time_value).strip().split(":", 1)
        hour = int(hour_str)
        minute = int(minute_str)
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            return 10_000
        return hour * 60 + minute
    except (ValueError, AttributeError):
        return 10_000


def prompt_days(prompt):
    return normalize_days(prompt.get("days"), prompt.get("day"))


def prompt_sort_key(prompt):
    days = prompt_days(prompt)
    first_day = days[0] if days else ""
    day_index = DAY_ORDER.index(first_day) if first_day in DAY_ORDER else len(DAY_ORDER)
    return (
        day_index,
        time_to_minutes(prompt.get("start", "00:00")),
        time_to_minutes(prompt.get("end", "00:00")),
        prompt.get("show", ""),
    )


def migrate_prompt_record(prompt):
    normalized_days = prompt_days(prompt)
    migrated = dict(prompt)
    migrated["days"] = normalized_days
    migrated["day"] = normalized_days[0] if normalized_days else ""
    return migrated


def prompt_is_valid_for_moment(prompt, now=None):
    now = now or datetime.now()
    current_day = EN_WEEKDAY_TO_DAY.get(now.strftime("%A").lower(), "")
    current_minutes = time_to_minutes(now.strftime("%H:%M"))

    if not prompt.get("active", True):
        return False

    days = prompt_days(prompt)
    if days and current_day not in days:
        return False

    return time_to_minutes(prompt.get("start", "00:00")) <= current_minutes <= time_to_minutes(
        prompt.get("end", "00:00")
    )
