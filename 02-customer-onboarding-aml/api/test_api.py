from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

VALID_CUSTOMER = {
    "name": "Ahmed Ali",
    "age": 30,
    "nationality": "SA",
    "is_pep": False,
    "id_expiry": "2027-01-01",
}


def onboard(**changes):
    body = dict(VALID_CUSTOMER)
    body.update(changes)
    return client.post("/onboard", json=body)


# ===== منطق البزنس =====
def test_valid_customer_is_approved():
    r = onboard()
    assert r.status_code == 200
    assert r.json()["decision"] == "Approve"

def test_sanctioned_name_with_spaces_and_case():
    r = onboard(name="  omar   KHALID ")
    assert r.json()["decision"] == "Reject: sanctions match"

def test_under_18_is_rejected():
    assert onboard(age=17).json()["decision"] == "Reject: under 18"

def test_pep_needs_edd():
    assert onboard(is_pep=True).json()["decision"] == "EDD"


# ===== حدود العمر =====
def test_age_0_is_valid_data_but_under_18():
    r = onboard(age=0)
    assert r.status_code == 200
    assert r.json()["decision"] == "Reject: under 18"

def test_age_120_is_accepted():
    assert onboard(age=120).status_code == 200

def test_age_121_is_rejected():
    assert onboard(age=121).status_code == 422

def test_negative_age_is_rejected():
    assert onboard(age=-5).status_code == 422


# ===== صحة البيانات =====
def test_age_as_text_is_rejected():
    assert onboard(age="abc").status_code == 422

def test_wrong_date_format_is_rejected():
    assert onboard(id_expiry="01-09-2027").status_code == 422

def test_impossible_date_is_rejected():
    assert onboard(id_expiry="2027-02-30").status_code == 422

def test_missing_field_is_rejected():
    body = dict(VALID_CUSTOMER)
    del body["nationality"]
    assert client.post("/onboard", json=body).status_code == 422
    
def test_high_risk_country_in_lowercase_needs_edd():
    assert onboard(nationality="xa").json()["decision"] == "EDD"