TODAY = "2026-09-26"
SANCTIONS_LIST = ["Omar Khalid", "Salem Nasser", "Tariq Mansour"]
HIGH_RISK_COUNTRIES = ["XA", "XB"]


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
    for s in SANCTIONS_LIST:
        clean_list.append(normalize(s))
    return normalize(name) in clean_list


def get_decision(customer):
    if is_sanctioned(customer["name"]):
        return "Reject: sanctions match"

    eligibility = check_eligibility(customer)
    if eligibility != "Eligible":
        return eligibility

    nationality = customer["nationality"].strip().upper()
    if customer["is_pep"] or nationality in HIGH_RISK_COUNTRIES:
        return "EDD"

    return "Approve"