from datetime import date
from copy import deepcopy


def compute_age(date_of_birth: str) -> int:
    """
    Compute age in years from a date of birth string.

    :param date_of_birth: Date of birth in ISO format (YYYY-MM-DD).
    :type date_of_birth: str
    :return: Age in years.
    :rtype: int
    """
    date_of_birth = date.fromisoformat(date_of_birth)
    today = date.today()

    return today.year - date_of_birth.year \
        - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


def months_between(start: date, end: date) -> int:
    """
    Calculate the number of months between two dates, inclusive.

    :param start: Start date.
    :type start: date
    :param end: End date.
    :type end: date
    :return: Number of months between start and end dates.
    :rtype: int
    """
    return (end.year - start.year) * 12 + (end.month - start.month + 1)


def compute_experience_years(experiences: list[dict]) -> float:
    """
    Compute total years of experience from a list of employment experiences.
    
    :param experiences: List of employment experiences with start_date and end_date.
    :type experiences: list[dict]
    :return: Total years of experience as a 1 decimal float.
    :rtype: float
    """
    total_months = 0

    for exp in experiences:
        start = date.fromisoformat(exp["start_date"])
        end = date.fromisoformat(exp["end_date"]) if exp["end_date"] else date.today()
        total_months += max(0, months_between(start, end))

    total_years = total_months / 12
    return round(total_years, 1)


def seniority_from_years(years: float) -> str:
    """
    Determine seniority level based on years of experience.
    
    :param years: Total years of experience as a 1 decimal float.
    :type years: float
    :return: Seniority level ("junior", "mid", "senior", or "staff/principal").
    :rtype: str
    """
    if years < 2:
        return "junior"
    elif years < 5:
        return "mid"
    elif years < 8:
        return "senior"
    else:
        return "staff/principal"


def post_process(result: dict) -> dict:
    """
    Post-process the extraction result to add derived fields.

    :param result: Extraction result dictionary.
    :type result: dict
    :return: Post-processed extraction result dictionary.
    :rtype: dict
    """
    enriched = deepcopy(result)
    enriched["age"] = compute_age(result["birth_date"])
    enriched["experience_years"] = compute_experience_years(result["employment_dates"])
    enriched["seniority"] = seniority_from_years(enriched["experience_years"])
    return enriched