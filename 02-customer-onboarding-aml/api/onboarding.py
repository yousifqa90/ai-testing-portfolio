from database import get_high_risk_countries, get_sanctions_names
TODAY = "2026-10-01"
def check_eligibility(customer):
    if customer["age"] < 18:
        return "Reject: under 18"
    if customer["id_expiry"] < TODAY:
        return "Reject: ID expired"
    return "Eligible"


def normalize(name):
    return " ".join(name.split()).lower()


def is_sanctioned(name):
    clean_list = []
    for s in get_sanctions_names():
        clean_list.append(normalize(s))
    return normalize(name) in clean_list


def get_decision(customer):
    if is_sanctioned(customer["name"]):
        return "Reject: sanctions match"

    eligibility = check_eligibility(customer)
    if eligibility != "Eligible":
        return eligibility

    nationality = customer["nationality"].strip().upper()
    if customer["is_pep"] or nationality in get_high_risk_countries():
        return "EDD"

    return "Approve"